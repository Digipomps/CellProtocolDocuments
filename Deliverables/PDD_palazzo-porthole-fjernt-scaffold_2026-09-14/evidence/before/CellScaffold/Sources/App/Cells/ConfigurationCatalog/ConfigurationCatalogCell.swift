// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

//
//  ConfigurationCatalogCell.swift
//
//  Created by Codex on 11/02/2026.
//

import Foundation
import CellBase

final class ConfigurationCatalogCell: GeneralCell, PortholeRuntimeBindingEnsuring {
    private enum MenuSlot: String, Codable, CaseIterable {
        case upperLeft
        case upperMid
        case upperRight
        case lowerLeft
        case lowerMid
        case lowerRight

        var keypath: String { "\(rawValue)Menu" }
    }

    private struct CatalogEntry: Codable {
        var id: String
        var sourceCellEndpoint: String
        var sourceCellName: String
        var purpose: String
        var purposeDescription: String?
        var interests: [String]
        var menuSlots: [MenuSlot]
        var goal: CellConfiguration
        var configuration: CellConfiguration
        var updatedAt: Double

        func asObject() -> Object {
            var object: Object = [
                "id": .string(id),
                "sourceCellEndpoint": .string(sourceCellEndpoint),
                "sourceCellName": .string(sourceCellName),
                "purpose": .string(purpose),
                "interests": .list(interests.map { .string($0) }),
                "menuSlots": .list(menuSlots.map { .string($0.rawValue) }),
                "goal": .cellConfiguration(goal),
                "configuration": .cellConfiguration(configuration),
                "updatedAt": .float(updatedAt)
            ]
            if let purposeDescription {
                object["purposeDescription"] = .string(purposeDescription)
            }
            return object
        }
    }

    private struct CatalogPayload {
        var id: String?
        var sourceCellEndpoint: String
        var sourceCellName: String
        var purpose: String
        var purposeDescription: String?
        var interests: [String]
        var menuSlots: [MenuSlot]
        var goal: CellConfiguration
        var configuration: CellConfiguration
    }

    private struct ScaffoldPurposeTemplate {
        var sourceCellEndpoint: String
        var sourceCellName: String
        var purpose: String
        var purposeDescription: String
        var interests: [String]
        var menuSlots: [MenuSlot]
        var goal: CellConfiguration
        var configuration: CellConfiguration
    }

    private struct RemoteEventConfigurationAccessRequirement {
        var eventID: String
        var configurationName: String
        var sourceCellEndpoint: String
        var grantKeypath: String
        var grantPermission: String
        var agreementName: String
        var purposeRef: String
        var publicReleaseFlag: String
        var summary: String

        func asObject(publiclyReleased: Bool) -> Object {
            [
                "eventID": .string(eventID),
                "configurationName": .string(configurationName),
                "sourceCellEndpoint": .string(sourceCellEndpoint),
                "grantKeypath": .string(grantKeypath),
                "grantPermission": .string(grantPermission),
                "agreementName": .string(agreementName),
                "purposeRef": .string(purposeRef),
                "publicReleaseFlag": .string(publicReleaseFlag),
                "status": .string(publiclyReleased ? "public-release-open" : "agreement-required"),
                "summary": .string(summary)
            ]
        }
    }

    private static let arendalsukaPublicReleaseEnvironmentKey = "ARENDALSUKA_REMOTE_CONFIGURATION_ACCESS"
    private static let remoteEventConfigurationAccessRequirements: [RemoteEventConfigurationAccessRequirement] = [
        RemoteEventConfigurationAccessRequirement(
            eventID: "arendalsuka-2026",
            configurationName: "Arendalsuka Participant Program",
            sourceCellEndpoint: ArendalsukaConfigurationPublisherContract.endpoint,
            grantKeypath: "remoteEventConfigurations.arendalsuka2026.participantProgram",
            grantPermission: "r---",
            agreementName: "Arendalsuka participant program configuration access",
            purposeRef: "purpose://arendalsuka.participant.program.load",
            publicReleaseFlag: "\(arendalsukaPublicReleaseEnvironmentKey)=public",
            summary: "Allows a requester to discover and load the remote Arendalsuka participant CellConfiguration through the catalog."
        ),
        RemoteEventConfigurationAccessRequirement(
            eventID: "arendalsuka-2026",
            configurationName: "Arendalsuka Event Atlas",
            sourceCellEndpoint: "cell:///ArendalsukaEventAtlas",
            grantKeypath: "remoteEventConfigurations.arendalsuka2026.eventAtlas",
            grantPermission: "r---",
            agreementName: "Arendalsuka event atlas configuration access",
            purposeRef: "purpose://arendalsuka.event-atlas.inspect",
            publicReleaseFlag: "\(arendalsukaPublicReleaseEnvironmentKey)=public",
            summary: "Allows a requester to discover and load the remote Arendalsuka source/import atlas CellConfiguration through the catalog."
        )
    ]

    // Only publish configurations whose primary endpoint is known to load in a
    // regular porthole flow without extra owner-domain bootstrap.
    private static let portholeSupportedEndpoints: Set<String> = [
        "cell:///AdminDeploymentSupervisor",
        "cell:///AIGateway",
        "cell:///AIAssistantThread",
        "cell:///AdminOverview",
        "cell:///AgreementWorkbench",
        "cell:///ArendalsukaEventAtlas",
        "cell:///ArendalsukaConfigurationPublisher",
        "cell:///ArendalsukaParticipantProgram",
        "cell:///Chat",
        "cell:///CellConfigurationStudio",
        "cell:///CalendarStore",
        "cell:///ConfigurationCatalog",
        "cell:///ConferenceAdminPreviewShell",
        "cell:///ConferenceChatLaunch",
        "cell:///ConferenceDemoStory",
        "cell:///ConferenceOnboarding",
        "cell:///ConferenceParticipantShell",
        "cell:///ConferenceParticipantPreviewShell",
        "cell:///ConferencePublicProfile",
        "cell:///ConferencePublicProfileEditorPreview",
        "cell:///ConferencePublicProfilePreview",
        "cell:///ConferencePublicShell",
        "cell:///ConferenceSponsorPreviewShell",
        "cell:///EventActorDirectory",
        "cell:///EventAdminShell",
        "cell:///EventDirectoryAggregator",
        "cell:///EventFederationBroker",
        "cell:///EventPublicShell",
        "cell:///EventPublisherAdminShell",
        "cell:///EventPublisherOnboarding",
        "cell:///ExecutablePurposeGrounding",
        "cell:///ConferenceUIRouter",
        "cell:///DeviceRegistration",
        "cell:///DraftVersion",
        "cell:///EntitiesWrapper",
        "cell:///EntityCellGraph",
        "cell:///EntityStudio",
        "cell:///GitHubWorkSync",
        "cell:///IdeaTaskWorkspace",
        "cell:///MarkdownRenderer",
        "cell:///ParticipationHub",
        "cell:///PersonalChatHub",
        "cell:///PersonalCopilotConfigurationCatalog",
        "cell:///PersonalMatchmaking",
        "cell:///PersonalMeetingCoordinator",
        "cell:///PersonalPagePublisher",
        "cell:///PersonalProfilePublisher",
        "cell:///ProjectPortfolio",
        "cell:///PublicProfileDirectory",
        "cell:///QuestionnaireCampaign",
        "cell:///MermaidRenderer",
        "cell:///MediaCollection",
        "cell:///ArtistSalesChannel",
        "cell:///MusicPublishingConsole",
        "cell:///SMIAgreementSettlement",
        "cell:///PaymentProofDoor",
        "cell:///ConciergeKnowledgeCorpus",
        "cell:///PalazzoCommunaleConcierge",
        "cell:///RestaurantExperiencePlan",
        "cell:///RestaurantGuestShell",
        "cell:///RestaurantPublishedContent",
        "cell:///RestaurantStaffShell",
        "cell:///RAGCatalogIngestion",
        "cell:///RAGGateway",
        "cell:///RAGIngestMedia",
        "cell:///RAGPromptAdmin",
        "cell:///SalesWorkspace",
        "cell:///ScaffoldSetup",
        "cell:///SecurityWorkbench",
        "cell:///TrustPacket",
        "cell:///TrustPacketWorkbench",
        "cell:///FlowDebugProbe",
        "cell:///ServiceCatalog",
        "cell:///SoftwareDistribution",
        "cell:///TimesWrapper",
        "cell:///Todo",
        "cell:///Vault",
        "cell:///VaultStudio",
        "cell:///WorkbenchAccessGrant",
        "cell:///WorkItem"
    ]

    private static func stableUUID(seed: String) -> UUID {
        var high: UInt64 = 0xcbf29ce484222325
        var low: UInt64 = 0x84222325cbf29ce4
        for byte in seed.utf8 {
            high ^= UInt64(byte)
            high &*= 0x100000001b3
            low ^= UInt64(byte)
            low &*= 0x9e3779b185ebca87
        }
        return UUID(uuid: (
            UInt8((high >> 56) & 0xff),
            UInt8((high >> 48) & 0xff),
            UInt8((high >> 40) & 0xff),
            UInt8((high >> 32) & 0xff),
            UInt8((high >> 24) & 0xff),
            UInt8((high >> 16) & 0xff),
            UInt8((high >> 8) & 0xff),
            UInt8(high & 0xff),
            UInt8((low >> 56) & 0xff),
            UInt8((low >> 48) & 0xff),
            UInt8((low >> 40) & 0xff),
            UInt8((low >> 32) & 0xff),
            UInt8((low >> 24) & 0xff),
            UInt8((low >> 16) & 0xff),
            UInt8((low >> 8) & 0xff),
            UInt8(low & 0xff)
        ))
    }

    private static let conferencePortholePriorityNames: [String] = [
        "Conference Public Surface Claude",
        "Conference Participant Portal Claude",
        "Conference Participant Chat Claude",
        "Conference Control Tower Claude",
        "Conference Sponsor Follow-up Claude",
        "Conference Nearby Radar Claude",
        "Conference Control Tower",
        "Arendalsuka Participant Program",
        "Conference Participant Portal Dashboard",
        "Conference Demo Launcher",
        "Conference Registration Setup",
        "Conference Public Surface",
        "Conference Track Detail",
        "Conference Session Detail",
        "Conference Featured Person Detail",
        "Conference Participant Chat",
        "Conference Nearby Radar",
        "Conference Participant Portal Preview",
        "Conference Public Profile Editor",
        "Conference Public Profile",
        "Scaffold Setup & Identity Link"
    ]

    private static let conferencePortholePriorityByName: [String: Int] = Dictionary(
        uniqueKeysWithValues: conferencePortholePriorityNames.enumerated().map { ($0.element, $0.offset) }
    )

    enum CodingKeys: CodingKey {
        case generalCell
        case owner
        case entries
    }

    private let stateQueue = DispatchQueue(label: "ConfigurationCatalogCell.State")
    private var entriesByID: [String: CatalogEntry] = [:]

    required init(owner: Identity) async {
        await super.init(owner: owner)
        await setupRuntimeBindings(owner: owner)
    }

    required init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        try super.init(from: decoder)
        self.entriesByID = (try? container.decode([String: CatalogEntry].self, forKey: .entries)) ?? [:]
        _ = try container.decodeIfPresent(Identity.self, forKey: .owner)
    }

    override func installCellRuntimeBindingsForAccess() async throws {
        guard await installRuntimeBindings(requester: storedOwnerIdentity) else {
            throw PortholeRuntimeBindingInstallationError.persistedOwnerHomeVaultUnavailable
        }
    }

    override func encode(to encoder: Encoder) throws {
        try super.encode(to: encoder)
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(entriesByID, forKey: .entries)
    }

    private func setupPermissions(owner: Identity) async {
        agreementTemplate.addGrant("r---", for: "state")
        agreementTemplate.addGrant("r---", for: "configurations")
        agreementTemplate.addGrant("r---", for: "catalogEntries")
        agreementTemplate.addGrant("r---", for: "catalogContracts")
        agreementTemplate.addGrant("r---", for: "remoteEventAccessRequirements")
        Self.remoteEventConfigurationAccessRequirements.forEach { requirement in
            agreementTemplate.addGrant(requirement.grantPermission, for: requirement.grantKeypath)
        }
        MenuSlot.allCases.forEach { agreementTemplate.addGrant("r---", for: $0.keypath) }
        agreementTemplate.addGrant("rw--", for: "addConfiguration")
        agreementTemplate.addGrant("rw--", for: "editConfiguration")
        agreementTemplate.addGrant("rw--", for: "updateConfiguration")
        agreementTemplate.addGrant("rw--", for: "removeConfiguration")
        agreementTemplate.addGrant("rw--", for: "match")
        agreementTemplate.addGrant("rw--", for: "matchPrompt")
        agreementTemplate.addGrant("rw--", for: "matchPurpose")
        agreementTemplate.addGrant("rw--", for: "matchInterests")
        agreementTemplate.addGrant("rw--", for: "syncScaffoldPurposeGoals")
        agreementTemplate.addGrant("r---", for: "feed")
    }

    func ensurePortholeRuntimeBindings(requester: Identity) async {
        _ = await installRuntimeBindings(requester: requester)
    }

    private func installRuntimeBindings(requester: Identity) async -> Bool {
        let runtimeOwner = await portholeRuntimeOwner(requester: requester)
        return await setupRuntimeBindings(owner: runtimeOwner)
    }

    @discardableResult
    private func setupRuntimeBindings(owner: Identity) async -> Bool {
        await installPortholeRuntimeBindings(
            owner: owner,
            installPermissions: { [weak self] owner in
                await self?.setupPermissions(owner: owner)
            },
            installRuntime: { [weak self] owner in
                guard let self else { return }
                await self.setupKeys(owner: owner)
                await self.bootstrapDefaultsIfNeeded(requester: owner)
            }
        )
    }

    private func setupKeys(owner: Identity) async {
        await registerGet(key: "state", owner: owner) { [weak self] requester in
            guard let self = self else { return .null }
            guard await self.validateAccess("r---", at: "state", for: requester) else { return .string("denied") }
            return self.stateValue()
        }

        await registerGet(key: "configurations", owner: owner) { [weak self] requester in
            guard let self = self else { return .null }
            guard await self.validateAccess("r---", at: "configurations", for: requester) else { return .string("denied") }
            let entries = await self.accessibleEntries(self.sortedEntries(), requester: requester)
            let configurations = await self.overlayConfigurations(
                entries.map(\.configuration)
                    + WorkbenchAccessGrantCell.requesterSharedConfigurations(for: requester),
                requester: requester
            )
            return .list(configurations.map { .cellConfiguration($0) })
        }

        await registerGet(key: "catalogEntries", owner: owner) { [weak self] requester in
            guard let self = self else { return .null }
            guard await self.validateAccess("r---", at: "catalogEntries", for: requester) else { return .string("denied") }
            let entries = await self.overlayEntries(
                await self.accessibleEntries(self.sortedEntries(), requester: requester),
                requester: requester
            )
            return .list(entries.map { .object($0.asObject()) })
        }

        await registerGet(key: "catalogContracts", owner: owner) { [weak self] requester in
            guard let self = self else { return .null }
            guard await self.validateAccess("r---", at: "catalogContracts", for: requester) else { return .string("denied") }
            let entries = await self.overlayEntries(
                await self.accessibleEntries(self.sortedEntries(), requester: requester),
                requester: requester
            )
            return .list(entries.map { .object(Self.makeContractObject(for: $0)) })
        }

        await registerGet(key: "remoteEventAccessRequirements", owner: owner) { [weak self] requester in
            guard let self = self else { return .null }
            guard await self.validateAccess("r---", at: "remoteEventAccessRequirements", for: requester) else { return .string("denied") }
            let publiclyReleased = Self.remoteEventConfigurationsArePubliclyReleased()
            var rows = [ValueType]()
            rows.reserveCapacity(Self.remoteEventConfigurationAccessRequirements.count)
            for requirement in Self.remoteEventConfigurationAccessRequirements {
                let decision = await self.authorizationDecision(
                    requestedAccess: requirement.grantPermission,
                    at: requirement.grantKeypath,
                    for: requester
                )
                var object = requirement.asObject(publiclyReleased: publiclyReleased)
                object["requesterAccess"] = .bool(publiclyReleased || decision.allowed)
                object["authorizationReasonCode"] = .string(decision.reasonCode ?? "unspecified")
                object["requiredAction"] = .string(decision.requiredAction ?? "none")
                rows.append(.object(object))
            }
            return .list(rows)
        }

        for slot in MenuSlot.allCases {
            await registerGet(key: slot.keypath, owner: owner) { [weak self] requester in
                guard let self = self else { return .null }
                guard await self.validateAccess("r---", at: slot.keypath, for: requester) else { return .string("denied") }
                let entries = await self.accessibleEntries(
                    self.sortedEntries().filter { $0.menuSlots.contains(slot) },
                    requester: requester
                )
                let configurations = await self.overlayConfigurations(
                    entries.map(\.configuration),
                    requester: requester
                )
                return .list(configurations.map { .cellConfiguration($0) })
            }
        }

        await registerSet(key: "addConfiguration", owner: owner) { [weak self] requester, payload in
            guard let self = self else { return .null }
            guard await self.validateAccess("rw--", at: "addConfiguration", for: requester) else { return .string("denied") }
            return .string("deprecated: edit owning cell configuration instead")
        }

        await registerSet(key: "editConfiguration", owner: owner) { [weak self] requester, payload in
            guard let self = self else { return .null }
            guard await self.validateAccess("rw--", at: "editConfiguration", for: requester) else { return .string("denied") }
            return .string("deprecated: edit owning cell configuration instead")
        }

        await registerSet(key: "updateConfiguration", owner: owner) { [weak self] requester, payload in
            guard let self = self else { return .null }
            guard await self.validateAccess("rw--", at: "updateConfiguration", for: requester) else { return .string("denied") }
            return .string("deprecated: edit owning cell configuration instead")
        }

        await registerSet(key: "removeConfiguration", owner: owner) { [weak self] requester, payload in
            guard let self = self else { return .null }
            guard await self.validateAccess("rw--", at: "removeConfiguration", for: requester) else { return .string("denied") }
            return .string("deprecated: edit owning cell configuration instead")
        }

        await registerSet(key: "matchPurpose", owner: owner) { [weak self] requester, payload in
            guard let self = self else { return .null }
            guard await self.validateAccess("rw--", at: "matchPurpose", for: requester) else { return .string("denied") }
            guard let purposeTerm = self.extractPurposeTerm(payload), !purposeTerm.isEmpty else {
                return .list([])
            }
            let result = await self.matchConfigurations(purpose: purposeTerm, interests: nil, menuSlot: nil, limit: nil, requester: requester)
            return .list(result.map { .cellConfiguration($0.configuration) })
        }

        await registerSet(key: "matchInterests", owner: owner) { [weak self] requester, payload in
            guard let self = self else { return .null }
            guard await self.validateAccess("rw--", at: "matchInterests", for: requester) else { return .string("denied") }
            guard let interests = self.extractInterests(payload), !interests.isEmpty else {
                return .list([])
            }
            let result = await self.matchConfigurations(purpose: nil, interests: interests, menuSlot: nil, limit: nil, requester: requester)
            return .list(result.map { .cellConfiguration($0.configuration) })
        }

        await registerSet(key: "match", owner: owner) { [weak self] requester, payload in
            guard let self = self else { return .null }
            guard await self.validateAccess("rw--", at: "match", for: requester) else { return .string("denied") }
            let purpose = self.extractPurposeTerm(payload)
            let interests = self.extractInterests(payload)
            let menuSlot = self.extractMenuSlot(payload)
            let limit = self.extractLimit(payload)
            let result = await self.matchConfigurations(purpose: purpose, interests: interests, menuSlot: menuSlot, limit: limit, requester: requester)
            return .list(result.map { .cellConfiguration($0.configuration) })
        }

        await registerSet(key: "matchPrompt", owner: owner) { [weak self] requester, payload in
            guard let self = self else { return .null }
            guard await self.validateAccess("rw--", at: "matchPrompt", for: requester) else { return .string("denied") }
            return await self.matchPromptValue(payload, requester: requester)
        }

        await registerSet(key: "syncScaffoldPurposeGoals", owner: owner) { [weak self] requester, _ in
            guard let self = self else { return .null }
            guard await self.validateAccess("rw--", at: "syncScaffoldPurposeGoals", for: requester) else { return .string("denied") }
            let importedCount = await self.syncScaffoldPurposeGoals(requester: requester)
            await self.emitCatalogEvent(operation: "syncScaffoldPurposeGoals", entry: nil, requester: requester)
            var result: Object = [:]
            result["importedCount"] = .integer(importedCount)
            result["state"] = self.stateValue()
            return .object(result)
        }
    }

    override func validateCellSpecificAccess(_ requestedAccess: String, at keypath: String, for identity: Identity) async -> Bool {
        await scaffoldSurfaceGateAllows(
            requestedAccess,
            at: keypath,
            for: identity,
            surfaceName: "ConfigurationCatalog"
        )
    }

    private func stateValue() -> ValueType {
        let entries = sortedEntries()
        var object: Object = [:]
        object["count"] = .integer(entries.count)
        object["purposes"] = .list(Array(Set(entries.map { $0.purpose })).sorted().map { .string($0) })
        for slot in MenuSlot.allCases {
            let count = entries.filter { $0.menuSlots.contains(slot) }.count
            object["\(slot.rawValue)Count"] = .integer(count)
        }
        return .object(object)
    }

    private func sortedEntries() -> [CatalogEntry] {
        stateQueue.sync {
            entriesByID.values.sorted {
                if $0.purpose == $1.purpose {
                    return $0.configuration.name.localizedCaseInsensitiveCompare($1.configuration.name) == .orderedAscending
                }
                return $0.purpose.localizedCaseInsensitiveCompare($1.purpose) == .orderedAscending
            }
        }
    }

    private func overlayConfigurations(
        _ configurations: [CellConfiguration],
        requester: Identity
    ) async -> [CellConfiguration] {
        var result = [CellConfiguration]()
        result.reserveCapacity(configurations.count)
        for configuration in configurations {
            guard Self.shouldOverlayCatalogConfiguration(configuration) else {
                result.append(configuration)
                continue
            }
            let overlayed = await EditableCellConfigurationOverlayResolver.overlay(
                configuration: configuration,
                requester: requester
            )
            result.append(Self.configurationCatalogFacade(for: configuration, overlayed: overlayed))
        }
        return result
    }

    private func accessibleEntries(
        _ entries: [CatalogEntry],
        requester: Identity
    ) async -> [CatalogEntry] {
        var result = [CatalogEntry]()
        result.reserveCapacity(entries.count)
        for entry in entries {
            if await isCatalogEntryAccessible(entry, requester: requester) {
                result.append(entry)
            }
        }
        return result
    }

    private func isCatalogEntryAccessible(
        _ entry: CatalogEntry,
        requester: Identity
    ) async -> Bool {
        guard let requirement = Self.remoteEventConfigurationAccessRequirement(for: entry) else {
            return true
        }
        if Self.remoteEventConfigurationsArePubliclyReleased() {
            return true
        }
        let decision = await authorizationDecision(
            requestedAccess: requirement.grantPermission,
            at: requirement.grantKeypath,
            for: requester
        )
        return decision.allowed
    }

    private static func remoteEventConfigurationAccessRequirement(
        for entry: CatalogEntry
    ) -> RemoteEventConfigurationAccessRequirement? {
        remoteEventConfigurationAccessRequirements.first { requirement in
            entry.sourceCellEndpoint == requirement.sourceCellEndpoint
                || entry.configuration.discovery?.sourceCellEndpoint == requirement.sourceCellEndpoint
                || entry.configuration.name == requirement.configurationName
        }
    }

    private static func remoteEventConfigurationsArePubliclyReleased() -> Bool {
        let raw = ProcessInfo.processInfo.environment[arendalsukaPublicReleaseEnvironmentKey]
            ?? ProcessInfo.processInfo.environment["ARENDALSUKA_PARTICIPANT_CONFIGURATION_PUBLIC"]
            ?? ""
        let normalized = raw.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        return ["1", "true", "yes", "public", "open", "released"].contains(normalized)
    }

    private func overlayEntries(
        _ entries: [CatalogEntry],
        requester: Identity
    ) async -> [CatalogEntry] {
        var result = [CatalogEntry]()
        result.reserveCapacity(entries.count)
        for entry in entries {
            guard Self.shouldOverlayCatalogConfiguration(entry.configuration) else {
                result.append(entry)
                continue
            }
            let overlayedConfiguration = await EditableCellConfigurationOverlayResolver.overlay(
                configuration: entry.configuration,
                requester: requester
            )
            var overlayedEntry = entry
            overlayedEntry.configuration = Self.configurationCatalogFacade(
                for: entry.configuration,
                overlayed: overlayedConfiguration
            )
            overlayedEntry.goal = overlayedConfiguration
            result.append(overlayedEntry)
        }
        return result
    }

    private static func shouldOverlayCatalogConfiguration(_ configuration: CellConfiguration) -> Bool {
        switch configuration.name {
        case "Conference Participant Portal Dashboard",
             "Conference Control Tower",
             "Conference Sponsor Follow-up",
             "Conference Public Profile Editor":
            return true
        default:
            return false
        }
    }

    private static func configurationCatalogFacade(
        for catalogConfiguration: CellConfiguration,
        overlayed: CellConfiguration
    ) -> CellConfiguration {
        var facade = overlayed
        facade.uuid = catalogConfiguration.uuid
        facade.name = catalogConfiguration.name
        facade.description = catalogConfiguration.description
        facade.discovery = catalogConfiguration.discovery
        return facade
    }

    private static func makeContractObject(for entry: CatalogEntry) -> Object {
        var contract: Object = [
            "id": .string(entry.id),
            "sourceCellEndpoint": .string(entry.sourceCellEndpoint),
            "sourceCellName": .string(entry.sourceCellName),
            "purpose": .string(entry.purpose),
            "interests": .list(entry.interests.map(ValueType.string)),
            "menuSlots": .list(entry.menuSlots.map { .string($0.rawValue) }),
            "displayName": .string(entry.configuration.name),
            "summary": .string(entry.configuration.description ?? ""),
            "categoryPath": .list(categoryPath(for: entry).map(ValueType.string)),
            "tags": .list(tags(for: entry).map(ValueType.string)),
            "purposeRefs": .list(purposeRefs(for: entry).map(ValueType.string)),
            "interestRefs": .list(entry.interests.map(ValueType.string)),
            "supportedInsertionModes": .list([.string("root")]),
            "supportedTargetKinds": .list(supportedTargetKinds(for: entry.configuration).map(ValueType.string)),
            "authRequired": .bool(entry.sourceCellEndpoint == "cell:///ScaffoldSetup" || remoteEventConfigurationAccessRequirement(for: entry) != nil),
            "policyHints": .list(policyHints(for: entry).map(ValueType.string)),
            "flowDriven": .bool(entry.configuration.cellReferences?.contains(where: { $0.subscribeFeed }) == true),
            "editable": .bool(entry.sourceCellEndpoint == "cell:///CellConfigurationStudio"),
            "recommendedContexts": .list(recommendedContexts(for: entry).map(ValueType.string)),
            "goal": .cellConfiguration(entry.goal),
            "configuration": .cellConfiguration(entry.configuration),
            "updatedAtEpochMs": .float(entry.updatedAt * 1000)
        ]
        if let purposeDescription = entry.purposeDescription, purposeDescription.isEmpty == false {
            contract["purposeDescription"] = .string(purposeDescription)
        }
        if let ioSignature = ioSignatureObject(for: entry) {
            contract["ioSignature"] = .object(ioSignature)
        } else {
            contract["ioSignature"] = .null
        }
        if let accessRequirement = remoteEventConfigurationAccessRequirement(for: entry) {
            contract["accessRequirement"] = .object(accessRequirement.asObject(
                publiclyReleased: remoteEventConfigurationsArePubliclyReleased()
            ))
        }
        return contract
    }

    private static func normalizedPurposeRefs(for purpose: String) -> [String] {
        purpose
            .lowercased()
            .split(whereSeparator: { $0.isWhitespace || $0 == "/" || $0 == "&" || $0 == "-" })
            .map(String.init)
            .filter { $0.isEmpty == false }
    }

    private static func purposeRefs(for entry: CatalogEntry) -> [String] {
        let explicitRefs = entry.interests.compactMap { interest -> String? in
            guard interest.hasPrefix("purposeRef=") else { return nil }
            let value = String(interest.dropFirst("purposeRef=".count))
                .trimmingCharacters(in: .whitespacesAndNewlines)
            return value.isEmpty ? nil : value
        }
        return dedupePreservingOrder(explicitRefs + normalizedPurposeRefs(for: entry.purpose))
    }

    private static func dedupePreservingOrder(_ values: [String]) -> [String] {
        var seen = Set<String>()
        var result = [String]()
        for value in values {
            let key = value.trimmingCharacters(in: .whitespacesAndNewlines)
            guard key.isEmpty == false else { continue }
            if seen.insert(key.lowercased()).inserted {
                result.append(key)
            }
        }
        return result
    }

    private static func supportedTargetKinds(for configuration: CellConfiguration) -> [String] {
        if configuration.skeleton != nil {
            return ["workspace", "skeleton"]
        }
        if configuration.cellReferences?.isEmpty == false {
            return ["workspace", "reference"]
        }
        return ["workspace"]
    }

    private static func recommendedContexts(for entry: CatalogEntry) -> [String] {
        var contexts = [String]()
        if entry.interests.contains(where: { $0.localizedCaseInsensitiveContains("binding") }) {
            contexts.append("binding")
        }
        if entry.interests.contains(where: { $0.localizedCaseInsensitiveContains("web") }) {
            contexts.append("web")
        }
        if entry.sourceCellEndpoint == "cell:///ScaffoldSetup" {
            contexts.append("admin")
        }
        if entry.sourceCellName.hasPrefix("SkeletonParity") {
            contexts.append(contentsOf: ["binding", "web"])
        }
        return Array(Set(contexts)).sorted()
    }

    private static func categoryPath(for entry: CatalogEntry) -> [String] {
        if entry.sourceCellEndpoint == "cell:///ScaffoldSetup" {
            return ["scaffold", "control-plane"]
        }
        if entry.sourceCellName.hasPrefix("SkeletonParity") {
            return ["scaffold", "skeleton-parity"]
        }
        return []
    }

    private static func tags(for entry: CatalogEntry) -> [String] {
        var tags = entry.interests
        if entry.sourceCellEndpoint == "cell:///ScaffoldSetup" {
            tags.append(contentsOf: ["identity-link", "scaffold"])
        }
        if entry.sourceCellName.hasPrefix("SkeletonParity") {
            tags.append(contentsOf: ["deterministic_fixture", "scaffold_owned"])
        }
        return Array(Set(tags)).sorted()
    }

    private static func policyHints(for entry: CatalogEntry) -> [String] {
        if remoteEventConfigurationAccessRequirement(for: entry) != nil {
            return remoteEventConfigurationsArePubliclyReleased()
                ? ["remote_event_configuration", "public_release_open"]
                : ["remote_event_configuration", "agreement_required"]
        }
        if entry.sourceCellEndpoint == "cell:///ScaffoldSetup" {
            return ["action_specific_authorization", "some_actions_require_admin_entry_proof"]
        }
        if entry.sourceCellName.hasPrefix("SkeletonParity") {
            return ["deterministic_fixture", "scaffold_owned"]
        }
        return []
    }

    private static func ioSignatureObject(for entry: CatalogEntry) -> Object? {
        if entry.sourceCellEndpoint == "cell:///ScaffoldSetup" {
            return [
                "getKeys": .list(["feed", "state"].map(ValueType.string)),
                "setKeys": .list([
                    "approveCurrentLinkChallenge",
                    "bootstrapOwner",
                    "createLinkChallenge",
                    "refresh",
                    "setIdentityLinkTransportBaseURL"
                ].map(ValueType.string)),
                "setPolicies": .object([
                    "setIdentityLinkTransportBaseURL": .list([
                        .string("requires_owner_proof"),
                        .string("requires_admin_entry_proof")
                    ])
                ]),
                "topics": .list([]),
                "filterTypes": .list([])
            ]
        }

        if entry.sourceCellName.hasPrefix("SkeletonParity") {
            var setKeys = ["dispatchAction", "resetFixture"]
            if entry.sourceCellName == "SkeletonParityFormFixture" {
                setKeys.append(contentsOf: ["setDraftBody", "setDraftTitle"])
            }

            return [
                "getKeys": .list(["purposeGoal", "skeletonConfiguration", "state"].map(ValueType.string)),
                "setKeys": .list(setKeys.map(ValueType.string)),
                "topics": .list([]),
                "filterTypes": .list([])
            ]
        }

        return nil
    }

    private func extractID(_ payload: ValueType) -> String? {
        switch payload {
        case .string(let id):
            return id
        case .object(let object):
            if case let .string(id)? = object["id"] {
                return id
            }
            if case let .string(id)? = object["uuid"] {
                return id
            }
            return nil
        default:
            return nil
        }
    }

    private func decodeCatalogPayload(_ payload: ValueType, requireID: Bool) -> CatalogPayload? {
        guard case let .object(object) = payload else { return nil }
        let id = extractID(payload)
        if requireID && (id == nil || id?.isEmpty == true) {
            return nil
        }

        guard let configuration = decodeConfiguration(from: object["configuration"]) else { return nil }

        let goal = decodeConfiguration(from: object["goal"]) ?? configuration

        let sourceCellEndpoint: String
        if case let .string(endpoint)? = object["sourceCellEndpoint"], !endpoint.isEmpty {
            sourceCellEndpoint = endpoint
        } else if let firstEndpoint = configuration.cellReferences?.first?.endpoint {
            sourceCellEndpoint = firstEndpoint
        } else {
            sourceCellEndpoint = "cell:///Unknown"
        }

        let sourceCellName: String
        if case let .string(name)? = object["sourceCellName"], !name.isEmpty {
            sourceCellName = name
        } else {
            sourceCellName = configuration.name
        }

        let purpose: String
        if case let .string(purposeName)? = object["purpose"], !purposeName.isEmpty {
            purpose = purposeName
        } else {
            purpose = configuration.name
        }

        let purposeDescription: String?
        if case let .string(description)? = object["purposeDescription"], !description.isEmpty {
            purposeDescription = description
        } else {
            purposeDescription = nil
        }

        let interests = extractInterestList(from: object["interests"]) ?? []
        let menuSlots = extractMenuSlots(from: object["menuSlots"]) ?? [.upperLeft]

        return CatalogPayload(
            id: id,
            sourceCellEndpoint: sourceCellEndpoint,
            sourceCellName: sourceCellName,
            purpose: purpose,
            purposeDescription: purposeDescription,
            interests: interests,
            menuSlots: menuSlots,
            goal: goal,
            configuration: configuration
        )
    }

    private func decodeConfiguration(from value: ValueType?) -> CellConfiguration? {
        guard let value else { return nil }
        switch value {
        case .cellConfiguration(let configuration):
            return configuration
        case .object(let object):
            guard let data = try? JSONEncoder().encode(object) else { return nil }
            return try? JSONDecoder().decode(CellConfiguration.self, from: data)
        default:
            return nil
        }
    }

    private func extractInterestList(from value: ValueType?) -> [String]? {
        guard let value else { return nil }
        switch value {
        case .string(let single):
            return [single]
        case .list(let list):
            return list.compactMap {
                if case let .string(s) = $0, !s.isEmpty {
                    return s
                }
                return nil
            }
        default:
            return nil
        }
    }

    private func extractMenuSlots(from value: ValueType?) -> [MenuSlot]? {
        guard let value else { return nil }
        switch value {
        case .string(let slot):
            if let parsed = parseMenuSlot(slot) {
                return [parsed]
            }
            return nil
        case .list(let list):
            let parsed = list.compactMap { current -> MenuSlot? in
                if case let .string(slot) = current {
                    return parseMenuSlot(slot)
                }
                return nil
            }
            return parsed.isEmpty ? nil : parsed
        default:
            return nil
        }
    }

    private func parseMenuSlot(_ slot: String) -> MenuSlot? {
        let cleaned = slot.replacingOccurrences(of: "Menu", with: "")
        return MenuSlot(rawValue: cleaned)
    }

    private func upsert(from payload: CatalogPayload, keepExistingIDWhenMissing: Bool) -> CatalogEntry {
        let resolvedID: String = {
            if let id = payload.id, !id.isEmpty {
                return id
            }
            if keepExistingIDWhenMissing {
                if let existing = sortedEntries().first(where: { $0.configuration.uuid == payload.configuration.uuid }) {
                    return existing.id
                }
            }
            return UUID().uuidString
        }()

        let updatedEntry = CatalogEntry(
            id: resolvedID,
            sourceCellEndpoint: payload.sourceCellEndpoint,
            sourceCellName: payload.sourceCellName,
            purpose: payload.purpose,
            purposeDescription: payload.purposeDescription,
            interests: payload.interests,
            menuSlots: payload.menuSlots,
            goal: payload.goal,
            configuration: payload.configuration,
            updatedAt: Date().timeIntervalSince1970
        )

        stateQueue.sync {
            entriesByID[resolvedID] = updatedEntry
        }
        return updatedEntry
    }

    private func remove(id: String) -> Bool {
        stateQueue.sync {
            entriesByID.removeValue(forKey: id) != nil
        }
    }

    private func extractPurposeTerm(_ payload: ValueType) -> String? {
        switch payload {
        case .string(let term):
            return term
        case .object(let object):
            if case let .string(term)? = object["purpose"] {
                return term
            }
            if case let .string(term)? = object["term"] {
                return term
            }
            return nil
        default:
            return nil
        }
    }

    private func extractInterests(_ payload: ValueType) -> [String]? {
        switch payload {
        case .list:
            return extractInterestList(from: payload)
        case .string(let value):
            return [value]
        case .object(let object):
            return extractInterestList(from: object["interests"])
        default:
            return nil
        }
    }

    private func extractMenuSlot(_ payload: ValueType) -> MenuSlot? {
        guard case let .object(object) = payload else { return nil }
        if case let .string(slotName)? = object["menuSlot"] {
            return parseMenuSlot(slotName)
        }
        return nil
    }

    private func extractLimit(_ payload: ValueType) -> Int? {
        guard case let .object(object) = payload else { return nil }
        if case let .integer(limit)? = object["limit"] {
            return max(1, limit)
        }
        if case let .number(limit)? = object["limit"] {
            return max(1, limit)
        }
        return nil
    }

    private struct PromptScaffoldCandidate {
        var id: String?
        var name: String?
        var endpoint: String?
        var label: String?

        var matchKey: String {
            [id, endpoint, name, label]
                .compactMap { $0?.trimmingCharacters(in: .whitespacesAndNewlines) }
                .first { $0.isEmpty == false }?
                .lowercased() ?? UUID().uuidString
        }

        func objectValue() -> Object {
            var object: Object = [:]
            object["id"] = id.map(ValueType.string) ?? .null
            object["name"] = name.map(ValueType.string) ?? .null
            object["endpoint"] = endpoint.map(ValueType.string) ?? .null
            object["label"] = label.map(ValueType.string) ?? .null
            return object
        }
    }

    private struct PromptMatchIntent {
        var id: String
        var purpose: String?
        var interests: [String]
        var requiresScaffoldContext: Bool
        var reason: String
    }

    private func matchPromptValue(_ payload: ValueType, requester: Identity) async -> ValueType {
        guard let prompt = extractPromptText(payload) else {
            return .object([
                "schemaVersion": .string("configurationCatalog.promptMatch.v1"),
                "status": .string("no_input"),
                "recommendedNextStep": .string("answer_text"),
                "loadSurface": .bool(false),
                "reason": .string("Prompt was empty.")
            ])
        }

        let intent = inferPromptIntent(prompt)
        let candidates = extractPromptScaffoldCandidates(payload)
        let selectedScaffold = selectedPromptScaffold(for: prompt, candidates: candidates)
        if intent.requiresScaffoldContext, selectedScaffold == nil {
            return .object([
                "schemaVersion": .string("configurationCatalog.promptMatch.v1"),
                "status": .string("needs_clarification"),
                "recommendedNextStep": .string("ask_clarification"),
                "loadSurface": .bool(false),
                "prompt": .string(prompt),
                "intent": .string(intent.id),
                "reason": .string("The prompt asks for scaffold-specific admin state, but the scaffold context is not unambiguous."),
                "question": .string("Hvilket scaffold mener du?"),
                "candidateScaffolds": .list(candidates.map { .object($0.objectValue()) }),
                "configurations": .list([])
            ])
        }

        let limit = extractLimit(payload) ?? 3
        let matches = await matchConfigurations(
            purpose: intent.purpose ?? prompt,
            interests: intent.interests,
            menuSlot: extractMenuSlot(payload),
            limit: limit,
            requester: requester
        )

        guard let primary = matches.first else {
            return .object([
                "schemaVersion": .string("configurationCatalog.promptMatch.v1"),
                "status": .string("no_match"),
                "recommendedNextStep": .string("answer_text"),
                "loadSurface": .bool(false),
                "prompt": .string(prompt),
                "intent": .string(intent.id),
                "reason": .string("No catalog configuration matched the prompt.")
            ])
        }

        var result: Object = [
            "schemaVersion": .string("configurationCatalog.promptMatch.v1"),
            "status": .string("matched"),
            "recommendedNextStep": .string("load_surface"),
            "loadSurface": .bool(true),
            "prompt": .string(prompt),
            "intent": .string(intent.id),
            "reason": .string(intent.reason),
            "inferredInterests": .list(intent.interests.map(ValueType.string)),
            "primaryConfigurationName": .string(primary.configuration.name),
            "primarySourceCellEndpoint": .string(primary.sourceCellEndpoint),
            "primarySourceCellName": .string(primary.sourceCellName),
            "configurationCount": .integer(matches.count),
            "configurations": .list(matches.map { .cellConfiguration($0.configuration) })
        ]
        result["selectedScaffold"] = selectedScaffold.map { .object($0.objectValue()) } ?? .null
        return .object(result)
    }

    private func extractPromptText(_ payload: ValueType) -> String? {
        let raw: String?
        switch payload {
        case .string(let prompt):
            raw = prompt
        case .object(let object):
            raw = stringValue(from: object["prompt"])
                ?? stringValue(from: object["query"])
                ?? stringValue(from: object["text"])
                ?? stringValue(from: object["utterance"])
                ?? stringValue(from: object["purpose"])
                ?? stringValue(from: object["term"])
        default:
            raw = nil
        }
        guard let trimmed = raw?.trimmingCharacters(in: .whitespacesAndNewlines),
              trimmed.isEmpty == false else {
            return nil
        }
        return trimmed
    }

    private func inferPromptIntent(_ prompt: String) -> PromptMatchIntent {
        let normalized = normalizePrompt(prompt)
        let adminTerms = ["admin", "operator", "operatør", "operatoer", "drift", "ops"]
        let loadTerms = ["lasten", "belastning", "systemlast", "prosesslast", "load", "cpu", "minne", "memory", "ram", "disk", "diskplass", "lagring", "storage", "kapasitet", "plass igjen"]
        let deploymentTerms = ["deploy", "deployment", "oppdater", "oppdatere", "ny versjon", "versjon", "drain", "blue-green", "blue green", "rollback", "restart", "rullering"]

        if containsAny(loadTerms, in: normalized) || asksForScaffoldLoad(normalized) {
            return PromptMatchIntent(
                id: "admin.scaffold.load.observe",
                purpose: "Admin kontrollplanoversikt",
                interests: [
                    "admin",
                    "operations",
                    "metrics",
                    "load",
                    "cpu",
                    "memory",
                    "disk",
                    "storage",
                    "capacity",
                    "host",
                    "processes",
                    "node-fleet",
                    "purposeRef=admin.scaffold-operations.observe"
                ],
                requiresScaffoldContext: true,
                reason: "Prompt asks for scaffold load or capacity, so the read-only control-plane overview is the safest first surface."
            )
        }

        if containsAny(deploymentTerms, in: normalized) {
            return PromptMatchIntent(
                id: "admin.scaffold.deployment.plan",
                purpose: "Admin drift",
                interests: [
                    "admin",
                    "operations",
                    "deployment",
                    "drain",
                    "blue-green",
                    "rollback",
                    "host",
                    "purposeRef=admin.scaffold-operations.observe"
                ],
                requiresScaffoldContext: true,
                reason: "Prompt asks for deployment state, so the operations workspace should load its read-only deployment supervisor projection."
            )
        }

        if containsAny(adminTerms, in: normalized) {
            return PromptMatchIntent(
                id: "admin.scaffold.open",
                purpose: "Admin kontrollplanoversikt",
                interests: ["admin", "operations", "overview", "readiness", "node-fleet"],
                requiresScaffoldContext: false,
                reason: "Prompt explicitly asks for admin functionality, so the control-plane overview is the least-privileged entry surface."
            )
        }

        return PromptMatchIntent(
            id: "catalog.prompt.match",
            purpose: nil,
            interests: [],
            requiresScaffoldContext: false,
            reason: "Prompt is routed through generic catalog purpose matching."
        )
    }

    private func extractPromptScaffoldCandidates(_ payload: ValueType) -> [PromptScaffoldCandidate] {
        guard case let .object(object) = payload else { return [] }
        var candidates = [PromptScaffoldCandidate]()

        appendPromptScaffoldCandidate(from: object["scaffold"], into: &candidates)
        appendPromptScaffoldCandidate(from: object["currentScaffold"], into: &candidates)
        appendPromptScaffoldCandidate(from: object["selectedScaffold"], into: &candidates)
        appendPromptScaffoldCandidates(from: object["scaffolds"], into: &candidates)
        appendPromptScaffoldCandidates(from: object["candidateScaffolds"], into: &candidates)

        if case let .object(context)? = object["context"] {
            appendPromptScaffoldCandidate(from: context["scaffold"], into: &candidates)
            appendPromptScaffoldCandidate(from: context["currentScaffold"], into: &candidates)
            appendPromptScaffoldCandidate(from: context["selectedScaffold"], into: &candidates)
            appendPromptScaffoldCandidates(from: context["scaffolds"], into: &candidates)
            appendPromptScaffoldCandidates(from: context["candidateScaffolds"], into: &candidates)
        }

        var seen = Set<String>()
        return candidates.filter { candidate in
            seen.insert(candidate.matchKey).inserted
        }
    }

    private func appendPromptScaffoldCandidates(from value: ValueType?, into candidates: inout [PromptScaffoldCandidate]) {
        guard case let .list(list)? = value else {
            appendPromptScaffoldCandidate(from: value, into: &candidates)
            return
        }
        for item in list {
            appendPromptScaffoldCandidate(from: item, into: &candidates)
        }
    }

    private func appendPromptScaffoldCandidate(from value: ValueType?, into candidates: inout [PromptScaffoldCandidate]) {
        guard let value else { return }
        switch value {
        case .string(let name):
            let trimmed = name.trimmingCharacters(in: .whitespacesAndNewlines)
            guard trimmed.isEmpty == false else { return }
            candidates.append(PromptScaffoldCandidate(id: nil, name: trimmed, endpoint: nil, label: nil))
        case .object(let object):
            let candidate = PromptScaffoldCandidate(
                id: stringValue(from: object["id"]) ?? stringValue(from: object["scaffoldID"]),
                name: stringValue(from: object["name"]) ?? stringValue(from: object["displayName"]),
                endpoint: stringValue(from: object["endpoint"]) ?? stringValue(from: object["sourceCellEndpoint"]),
                label: stringValue(from: object["label"])
            )
            if [candidate.id, candidate.name, candidate.endpoint, candidate.label].contains(where: { $0?.isEmpty == false }) {
                candidates.append(candidate)
            }
        default:
            return
        }
    }

    private func selectedPromptScaffold(for prompt: String, candidates: [PromptScaffoldCandidate]) -> PromptScaffoldCandidate? {
        if candidates.count == 1 {
            return candidates.first
        }
        guard candidates.isEmpty == false else {
            return nil
        }

        let normalizedPrompt = normalizePrompt(prompt)
        let matches = candidates.filter { candidate in
            [candidate.id, candidate.name, candidate.endpoint, candidate.label]
                .compactMap { $0 }
                .map(normalizePrompt)
                .contains { term in
                    term.isEmpty == false && normalizedPrompt.contains(term)
                }
        }
        return matches.count == 1 ? matches.first : nil
    }

    private func normalizePrompt(_ value: String) -> String {
        value
            .folding(options: [.caseInsensitive, .diacriticInsensitive], locale: .current)
            .lowercased()
    }

    private func containsAny(_ terms: [String], in normalizedPrompt: String) -> Bool {
        terms.contains { normalizedPrompt.contains(normalizePrompt($0)) }
    }

    private func asksForScaffoldLoad(_ normalizedPrompt: String) -> Bool {
        normalizedPrompt.contains("hva er last")
            || normalizedPrompt.contains("hvilken last")
            || normalizedPrompt.contains("last pa")
            || normalizedPrompt.contains("last for")
    }

    private func stringValue(from value: ValueType?) -> String? {
        guard case let .string(string)? = value else { return nil }
        let trimmed = string.trimmingCharacters(in: .whitespacesAndNewlines)
        return trimmed.isEmpty ? nil : trimmed
    }

    private func matchConfigurations(
        purpose: String?,
        interests: [String]?,
        menuSlot: MenuSlot?,
        limit: Int?,
        requester: Identity
    ) async -> [CatalogEntry] {
        let normalizedPurpose = purpose?.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        let normalizedInterestSet: Set<String> = Set((interests ?? []).map { $0.lowercased() })
        let candidateEntries = await accessibleEntries(sortedEntries(), requester: requester)

        let scored: [(CatalogEntry, Double)] = candidateEntries
            .filter { entry in
                if let menuSlot {
                    return entry.menuSlots.contains(menuSlot)
                }
                return true
            }
            .map { entry in
                var score = 0.0

                if let normalizedPurpose, !normalizedPurpose.isEmpty {
                    if entry.purpose.lowercased().contains(normalizedPurpose) {
                        score += 2.0
                    }
                    if entry.configuration.name.lowercased().contains(normalizedPurpose) {
                        score += 1.0
                    }
                    if entry.purposeDescription?.lowercased().contains(normalizedPurpose) == true {
                        score += 0.8
                    }
                }

                if !normalizedInterestSet.isEmpty {
                    let entryInterests = Set(entry.interests.map { $0.lowercased() })
                    let overlap = normalizedInterestSet.intersection(entryInterests)
                    if !overlap.isEmpty {
                        score += Double(overlap.count) / Double(normalizedInterestSet.count)
                    }
                }

                if normalizedPurpose == nil && normalizedInterestSet.isEmpty {
                    score += 0.1
                }

                return (entry, score)
            }
            .filter { pair in
                if normalizedPurpose != nil || !normalizedInterestSet.isEmpty {
                    return pair.1 > 0.0
                }
                return true
            }
            .sorted { lhs, rhs in
                if lhs.1 == rhs.1 {
                    return lhs.0.configuration.name.localizedCaseInsensitiveCompare(rhs.0.configuration.name) == .orderedAscending
                }
                return lhs.1 > rhs.1
            }

        if let limit {
            return Array(scored.prefix(limit).map(\.0))
        }
        return scored.map(\.0)
    }

    private func bootstrapDefaultsIfNeeded(requester: Identity) async {
        _ = await syncScaffoldPurposeGoals(requester: requester)
    }

    private func syncScaffoldPurposeGoals(requester: Identity) async -> Int {
        var importedCount = 0
        let templates = Self.scaffoldPurposeTemplates()

        for template in templates {
            let existingMatch = sortedEntries().first {
                $0.sourceCellEndpoint == template.sourceCellEndpoint && $0.purpose == template.purpose
            }

            let payload = CatalogPayload(
                id: existingMatch?.id,
                sourceCellEndpoint: template.sourceCellEndpoint,
                sourceCellName: template.sourceCellName,
                purpose: template.purpose,
                purposeDescription: template.purposeDescription,
                interests: template.interests,
                menuSlots: template.menuSlots,
                goal: template.goal,
                configuration: template.configuration
            )
            _ = upsert(from: payload, keepExistingIDWhenMissing: existingMatch != nil)
            importedCount += 1
        }

        // These templates are the source of truth for scaffold-shipped purpose
        // goals. Do not resolve each source cell here: catalog sync is called
        // from Porthole bootstrap, and resolving cells while the catalog is
        // being resolved can recursively load persisted cell graphs.
        return importedCount
    }

    private static func scaffoldPurposeTemplates() -> [ScaffoldPurposeTemplate] {
        let chatConfig = ChatCell.chatConfiguration()
        let calendarConfigs = CalendarSurfaceConfigurationFactory.catalogConfigurations()
        let timesConfig = singleReferenceConfiguration(
            name: "Times",
            endpoint: "cell:///TimesWrapper",
            label: "times",
            sourceCellName: "TimesWrapperCell",
            purpose: "Tidslinje og planlegging",
            purposeDescription: "Følg tidsbaserte hendelser i en feed.",
            interests: ["time", "events", "planning"],
            menuSlots: [.upperRight]
        )
        let entitiesConfig = singleReferenceConfiguration(
            name: "Entities",
            endpoint: "cell:///EntitiesWrapper",
            label: "entities",
            sourceCellName: "EntitiesWrapperCell",
            purpose: "Entitetsoversikt",
            purposeDescription: "Vis relaterte entiteter og hendelser.",
            interests: ["entities", "network", "people"],
            menuSlots: [.lowerLeft]
        )
        let leadVaultConfig = LeadVaultHarnessConfigurationFactory.makeCellConfiguration()
        let salesWorkspaceConfig = SalesWorkspaceConfigurationFactory.makeCellConfiguration()
        let accessRequirementPromptConfig = AccessRequirementPromptConfigurationFactory.makeCellConfiguration()
        let agreementWorkbenchConfig = AgreementWorkbenchConfigurationFactory.makeCellConfiguration()
        let securityWorkbenchConfig = SecurityWorkbenchConfigurationFactory.makeCellConfiguration()
        let trustPacketConfig = TrustPacketConfigurationFactory.makeCellConfiguration()
        let personalDataTrustPackageConfig = PersonalDataTrustPackageConfigurationFactory.makeCellConfiguration()
        let flowDebugProbeConfig = FlowDebugProbeConfigurationFactory.makeCellConfiguration()
        let workbenchAccessConfig = WorkbenchAccessGrantConfigurationFactory.makeCellConfiguration()
        let entityStudioConfig = EntityStudioConfigurationFactory.makeCellConfiguration()
        let participationHubConfig = ParticipationHubConfigurationFactory.makeCellConfiguration()
        let conferenceConfig = ConferenceMVPSkeletonFactory.makeCellConfiguration()
        let conferenceDemoStoryConfig = ConferenceDemoStoryConfigurationFactory.makeCellConfiguration()
        let conferenceDemoLauncherConfig = conferenceDemoLauncherConfiguration()
        let conferenceSkeletonLibraryConfig = conferenceSkeletonComponentLibraryConfiguration()
        let conferenceRegistrationSetupConfig = conferenceRegistrationSetupConfiguration()
        let conferencePublicSurfaceConfig = conferencePublicSurfaceConfiguration()
        let conferenceTrackDetailConfig = conferenceTrackDetailConfiguration()
        let conferenceSessionDetailConfig = conferenceSessionDetailConfiguration()
        let conferenceAgendaTrackDetailConfig = conferenceAgendaTrackDetailConfiguration()
        let conferenceAgendaSessionDetailConfig = conferenceAgendaSessionDetailConfiguration()
        let conferenceFeaturedPersonDetailConfig = conferenceFeaturedPersonDetailConfiguration()
        let conferenceParticipantPortalPreviewConfig = conferenceParticipantPortalPreviewConfiguration()
        let conferenceParticipantPortalConfig = conferenceParticipantPortalConfiguration()
        let conferenceParticipantChatConfig = conferenceParticipantChatConfiguration()
        let conferenceNearbyRadarConfig = conferenceNearbyRadarConfiguration()
        let conferencePublicProfileEditorConfig = conferencePublicProfileEditorConfiguration()
        let conferencePublicProfileConfig = conferencePublicProfileConfiguration()
        let conferenceControlTowerConfig = conferenceControlTowerConfiguration()
        let conferencePublicSurfaceClaudeConfig = conferencePublicSurfaceClaudeConfiguration()
        let conferenceParticipantPortalClaudeConfig = conferenceParticipantPortalClaudeConfiguration()
        let conferenceParticipantChatClaudeConfig = conferenceParticipantChatClaudeConfiguration()
        let conferenceControlTowerClaudeConfig = conferenceControlTowerClaudeConfiguration()
        let conferenceSponsorClaudeConfig = conferenceSponsorClaudeConfiguration()
        let conferenceNearbyRadarClaudeConfig = conferenceNearbyRadarClaudeConfiguration()
        let scaffoldSetupConfig = scaffoldSetupConfiguration()
        let configurationArchitectConfig = configurationArchitectWorkspaceConfiguration()
        let conferenceAIAssistantConfig = conferenceAIAssistantConfiguration()
        let adminControlPlaneOverviewConfig = adminControlPlaneOverviewConfiguration()
        let adminOperationsConfig = adminOperationsWorkspaceConfiguration()
        let adminSecurityConfig = adminSecurityWorkspaceConfiguration()
        let adminProductAdministrationConfig = adminProductAdministrationConfiguration()
        let adminCopilotConfig = adminCopilotWorkspaceConfiguration()
        let palazzoConciergeConfig = palazzoConciergeCopilotConfiguration()
        let palazzoCommunaleConfig = PalazzoCommunaleServiceConfigurationFactory.makeCellConfiguration()
        let palazzoGuestConfig = RestaurantShellConfigurationFactory.makeGuestConfiguration()
        let palazzoStaffConfig = RestaurantShellConfigurationFactory.makeStaffConfiguration()
        let conferenceSponsorConfig = ConferenceShellConfigurationFactory.makeSponsorConfiguration()
        let eventPublisherOnboardingConfig = EventPlatformShellConfigurationFactory.publisherOnboardingConfiguration()
        let eventDirectoryConfig = EventPlatformShellConfigurationFactory.directoryConfiguration()
        let eventPublisherAdminConfig = EventPlatformShellConfigurationFactory.publisherAdminConfiguration()
        let eventActorDirectoryConfig = EventPlatformShellConfigurationFactory.actorDirectoryConfiguration()
        let eventPublicSurfaceConfig = EventPlatformShellConfigurationFactory.eventPublicConfiguration()
        let eventAdminWorkspaceConfig = EventPlatformShellConfigurationFactory.eventAdminConfiguration()
        let eventFederationSearchConfig = EventPlatformShellConfigurationFactory.federationBrokerConfiguration()
        let arendalsukaParticipantProgramConfig = ArendalsukaEventAtlasConfigurationFactory.makeParticipantProgramConfiguration()
        let arendalsukaEventAtlasConfig = ArendalsukaEventAtlasConfigurationFactory.makeCellConfiguration()
        let aiGatewayConfig = AIGatewayConfigurationFactory.makeWorkspaceConfiguration()
        let ragConfig = RAGGatewayConfigurationFactory.makeWorkspaceConfiguration()
        let ragPromptAdminConfig = RAGPromptAdminConfigurationFactory.makeCellConfiguration()
        let innoragPromptAdminConfig = RAGPromptAdminConfigurationFactory.makeCellConfiguration(
            name: "Innorag Prompt Admin",
            description: "Admin workspace for innorag prompt profiles and delegated prompt admins.",
            purpose: "Innorag promptadministrasjon",
            purposeDescription: "Styr promptprofiler og runtime override for innovasjons-RAG-en.",
            interests: ["rag", "innovasjon", "prompts", "admin", "configuration", "operations"],
            menuSlots: ["upperMid", "lowerLeft"],
            initialCaseID: "innovasjon"
        )
        let docPromptAdminConfig = RAGPromptAdminConfigurationFactory.makeCellConfiguration(
            name: "Doc Prompt Admin",
            description: "Admin workspace for documentation RAG prompt profiles and delegated prompt admins.",
            purpose: "Dokumentasjons-RAG promptadministrasjon",
            purposeDescription: "Styr promptprofiler og runtime override for dokumentasjons-RAG-en.",
            interests: ["rag", "documentation", "prompts", "admin", "configuration", "operations"],
            menuSlots: ["upperMid", "lowerLeft"],
            initialCaseID: "dimy_docs"
        )
        let todoConfig = TodoCell.todoConfiguration()
        let todoPlannerConfig = todoPlannerCopilotConfiguration()
        let mermaidConfig = mermaidRendererConfiguration()
        let cellOwnershipMapConfig = cellOwnershipMapConfiguration()
        let conferenceOwnershipConfig = conferenceOwnershipDiagramConfiguration()
        let vaultConfig = vaultWorkspaceConfiguration()
        let vaultStudioConfig = vaultStudioWorkspaceConfiguration()
        let ideaTaskShareConfig = ideaTaskShareConfiguration()
        let ideaTaskWorkspaceConfig = ideaTaskWorkspaceConfiguration()
        let havenWorkbenchConfig = havenWorkbenchConfiguration()
        let workItemConfig = workItemTrackerConfiguration()
        let projectPortfolioConfig = projectPortfolioConfiguration()
        let githubWorkSyncConfig = githubWorkSyncConfiguration()
        let projectOperationsConfig = ProjectOperationsConfigurationFactory.makeWorkspaceConfiguration()
        let obsidianAIConfig = obsidianAIWorkspaceConfiguration()
        let stagingDemoConfig = obsidianMermaidStagingConfiguration()
        let catalogConfig = ConfigurationCatalogClient.makeCellConfiguration()
        let cellConfigurationStudioConfig = CellConfigurationStudioConfigurationFactory.makeCellConfiguration()
        let conferenceBroadcastStudioConfig = ConferenceBroadcastStudioConfigurationFactory.makeCellConfiguration()
        let consentReceiptConfig = singleReferenceConfiguration(
            name: "Consent Receipt Ledger",
            endpoint: "cell:///ConsentReceipt",
            label: "consentReceipt",
            sourceCellName: "ConsentReceiptCell",
            purpose: "Samtykkekvitteringer og receipts",
            purposeDescription: "Se og bruk lagrede consent receipts som del av lead- og agreement-flyt.",
            interests: ["consent", "receipts", "conference", "audit", "lead-vault"],
            menuSlots: [.upperMid, .lowerMid]
        )
        let exhibitorAccessConfig = singleReferenceConfiguration(
            name: "Exhibitor Access Gate",
            endpoint: "cell:///ExhibitorAccess",
            label: "exhibitorAccess",
            sourceCellName: "ExhibitorAccessCell",
            purpose: "Exhibitor-tilgang og entitlement",
            purposeDescription: "Vis og bruk exhibitor-access state som del av lead- og conference-flyt.",
            interests: ["conference", "exhibitor", "access", "entitlements", "lead-vault"],
            menuSlots: [.upperMid, .lowerMid]
        )
        let deviceRegistrationConfig = singleReferenceConfiguration(
            name: "Device Registration",
            endpoint: "cell:///DeviceRegistration",
            label: "deviceRegistration",
            sourceCellName: "DeviceRegistrationCell",
            purpose: "Enhetsregistrering for callbacks",
            purposeDescription: "Følg registrerte enheter og callback-klare klienter i conference-notification-flyt.",
            interests: ["conference", "devices", "callbacks", "notifications", "registration"],
            menuSlots: [.upperRight, .lowerRight]
        )
        let paymentGateConfig = singleReferenceConfiguration(
            name: "Payment Gate",
            endpoint: "cell:///PaymentGate",
            label: "paymentGate",
            sourceCellName: "PaymentGateCell",
            purpose: "Micropayment-gating og receipts",
            purposeDescription: "Quote, receipt og adgangsgating for ressurser som krever betaling eller prepaid saldo.",
            interests: ["payments", "micropayments", "receipts", "access", "commerce"],
            menuSlots: [.lowerRight]
        )
        let paymentProofDoorConfig = singleReferenceConfiguration(
            name: "Payment Proof Door",
            endpoint: "cell:///PaymentProofDoor",
            label: "paymentProofDoor",
            sourceCellName: "PaymentProofDoorCell",
            purpose: "Proof-gated adgang",
            purposeDescription: "Vis proof-kravet som må oppfylles for å komme gjennom en betalingsstyrt door.",
            interests: ["payments", "proofs", "entitlements", "agreements", "access"],
            menuSlots: [.lowerRight]
        )
        let smiAgreementSettlementConfig = SMIAgreementSettlementConfigurationFactory.makeCellConfiguration()
        let mediaCollectionConfig = MediaCollectionConfigurationFactory.makeCellConfiguration()
        let artistSalesConfig = ArtistSalesConfigurationFactory.makeCellConfiguration()
        let musicPublishingConfig = MusicPublishingConfigurationFactory.makeCellConfiguration()
        let webKnowledgeConfigs = WebKnowledgeConfigurationFactory.allConfigurations()
        let transcriptConfigs = TranscriptConfigurationFactory.allConfigurations()
        let spatialConfigs = SpatialConfigurationFactory.allConfigurations()
        let skeletonParityConfigs = SkeletonParityFixtures.catalogConfigurations()
        let personalCopilotConfigs = PersonalCopilotConfigurationFactory.catalogConfigurations()
        let personalEntityActivityConfigs = PersonalEntityActivityDashboardConfigurationFactory.catalogConfigurations()
        let calendarTemplates = calendarConfigs.map { config in
            scaffoldTemplate(
                configuration: config,
                fallbackSourceCellEndpoint: CalendarContract.endpoint,
                fallbackSourceCellName: CalendarContract.storeCellName,
                fallbackPurpose: config.discovery?.purpose ?? "Kalender og planlegging",
                fallbackPurposeDescription: config.discovery?.purposeDescription ?? "Vis canonical CalendarItem/CalendarOccurrence-data, importer/eksporter ICS og bruk portable calendar visualization med liste-fallback.",
                fallbackInterests: config.discovery?.interests ?? ["calendar", "schedule", "planning", "ics", "agenda", "recurrence"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            )
        }

        var templates: [ScaffoldPurposeTemplate] = calendarTemplates + [
            scaffoldTemplate(
                configuration: cellConfigurationStudioConfig,
                fallbackSourceCellEndpoint: "cell:///CellConfigurationStudio",
                fallbackSourceCellName: "CellConfigurationStudioCell",
                fallbackPurpose: "CellConfiguration redigering",
                fallbackPurposeDescription: "Finn source-backed konfigurasjoner via Library, hold working draft lokalt og apply tilbake til eiercellen.",
                fallbackInterests: ["configuration", "editing", "library", "skeleton", "binding", "web"],
                fallbackMenuSlots: [.upperLeft, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: chatConfig,
                fallbackSourceCellEndpoint: "cell:///Chat",
                fallbackSourceCellName: "ChatCell",
                fallbackPurpose: "Kommunikasjon og samarbeid",
                fallbackPurposeDescription: "Få delt meldinger i sanntid mellom deltakere.",
                fallbackInterests: ["chat", "communication", "collaboration"],
                fallbackMenuSlots: [.upperLeft, .upperMid]
            ),
            scaffoldTemplate(
                configuration: timesConfig,
                fallbackSourceCellEndpoint: "cell:///TimesWrapper",
                fallbackSourceCellName: "TimesWrapperCell",
                fallbackPurpose: "Tidslinje og planlegging",
                fallbackPurposeDescription: "Følg tidsbaserte hendelser i en feed.",
                fallbackInterests: ["time", "events", "planning"],
                fallbackMenuSlots: [.upperRight]
            ),
            scaffoldTemplate(
                configuration: entitiesConfig,
                fallbackSourceCellEndpoint: "cell:///EntitiesWrapper",
                fallbackSourceCellName: "EntitiesWrapperCell",
                fallbackPurpose: "Entitetsoversikt",
                fallbackPurposeDescription: "Vis relaterte entiteter og hendelser.",
                fallbackInterests: ["entities", "network", "people"],
                fallbackMenuSlots: [.lowerLeft]
            ),
            scaffoldTemplate(
                configuration: accessRequirementPromptConfig,
                fallbackSourceCellEndpoint: "cell:///AccessRequirementPrompt",
                fallbackSourceCellName: "AccessRequirementPromptCell",
                fallbackPurpose: "Godkjenne tilgangskrav i skeleton",
                fallbackPurposeDescription: "Vis en eksplisitt approve- eller deny-komponent nar en referert celle krever agreement-basert grant eller proof/VC før den kan brukes.",
                fallbackInterests: ["agreement", "permissions", "identity", "approval", "skeleton", "testing", "proofs", "vc"],
                fallbackMenuSlots: [.upperMid, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: leadVaultConfig,
                fallbackSourceCellEndpoint: "cell:///LeadVault",
                fallbackSourceCellName: "LeadVaultCell",
                fallbackPurpose: "Conference Lead Vault",
                fallbackPurposeDescription: "Lead capture, consent receipts, qualification, entitlement gating og audit/export.",
                fallbackInterests: ["conference", "leads", "consent", "entitlements", "audit", "sales-ops"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: salesWorkspaceConfig,
                fallbackSourceCellEndpoint: "cell:///SalesWorkspace",
                fallbackSourceCellName: "SalesWorkspaceCell",
                fallbackPurpose: "Sales workspace",
                fallbackPurposeDescription: "Account-scoped salg, lokal kontaktgraf, e-postmetadata og Todo-basert oppfolging.",
                fallbackInterests: ["sales", "crm", "follow-up", "email-bridge", "social-network", "todo", "cellprotocol-transition"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: mediaCollectionConfig,
                fallbackSourceCellEndpoint: MediaCollectionContract.endpoint,
                fallbackSourceCellName: MediaCollectionContract.sourceCellName,
                fallbackPurpose: "Delt mediesamling",
                fallbackPurposeDescription: "Samle bilde-, video-, lyd-, tekst- og lokasjonsreferanser fra inviterte deltakere med eksplisitte grants og cache-status.",
                fallbackInterests: ["media", "photos", "events", "guests", "attachments", "cache", "vc", "location", "ar"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: artistSalesConfig,
                fallbackSourceCellEndpoint: ArtistSalesContract.endpoint,
                fallbackSourceCellName: ArtistSalesContract.sourceCellName,
                fallbackPurpose: "Kunstutstillinger og salg",
                fallbackPurposeDescription: "Publiser kunst i støttede medier med offentlig preview, betalt inngang, separat verkpris, nedlasting og signert rettighetsbevis.",
                fallbackInterests: ["art", "exhibition", "media", "usage-quota", "access-entitlement", "rights-proof", "download"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: musicPublishingConfig,
                fallbackSourceCellEndpoint: "cell:///MusicPublishingConsole",
                fallbackSourceCellName: "MusicPublishingConsoleCell",
                fallbackPurpose: "Musikkpublisering",
                fallbackPurposeDescription: "Publiser musikk fra egne celler med katalog, access policy, HLS-leveranse og storage-adaptere.",
                fallbackInterests: ["music", "publishing", "streaming", "download", "hls", "micropayments", "storage"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: agreementWorkbenchConfig,
                fallbackSourceCellEndpoint: "cell:///AgreementWorkbench",
                fallbackSourceCellName: "AgreementWorkbenchCell",
                fallbackPurpose: "Avtaleverksted og tilgangsdesign",
                fallbackPurposeDescription: "Velg avtalemaler, forklar rettigheter i vanlig språk og pek til riktige keypaths før bruk i Binding eller andre scaffold.",
                fallbackInterests: ["agreement", "permissions", "conditions", "identity", "binding", "governance"],
                fallbackMenuSlots: [.upperMid, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: securityWorkbenchConfig,
                fallbackSourceCellEndpoint: "cell:///SecurityWorkbench",
                fallbackSourceCellName: "SecurityWorkbenchCell",
                fallbackPurpose: "Sikkerhetsobservasjon og autoriserte probes",
                fallbackPurposeDescription: "Vis CellSecurityKit-events, kjør lokale/staging-allowlist probes og styr lokal containment uten å gi tilgang.",
                fallbackInterests: ["security", "identity", "probes", "containment", "audit", "staging"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: trustPacketConfig,
                fallbackSourceCellEndpoint: TrustPacketWorkbenchContract.endpoint,
                fallbackSourceCellName: TrustPacketWorkbenchContract.sourceCellName,
                fallbackPurpose: "Tillitspakke og kvittering",
                fallbackPurposeDescription: "Vis grenser, formål, mottaker, varighet, AI/evidence, signatur, eksport og revoke før en tillitspakke deles.",
                fallbackInterests: ["trust-packet", "consent", "receipt", "signature", "provenance", "purpose", "privacy", "audit"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: personalDataTrustPackageConfig,
                fallbackSourceCellEndpoint: PersonalDataTrustPackageContract.endpoint,
                fallbackSourceCellName: PersonalDataTrustPackageContract.sourceCellName,
                fallbackPurpose: "Forhåndsvis behandling av persondata",
                fallbackPurposeDescription: "Vis forslag, kilder, planlagte eksterne kall, lagringstid og separate Entity-/delingsbeslutninger før handling.",
                fallbackInterests: ["personal-data", "provenance", "privacy", "http-transparency", "retention", "entity-control"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: flowDebugProbeConfig,
                fallbackSourceCellEndpoint: FlowDebugProbeContract.endpoint,
                fallbackSourceCellName: FlowDebugProbeContract.sourceCellName,
                fallbackPurpose: "Flow-debug og observasjon",
                fallbackPurposeDescription: "Observer FlowElements mellom celler, vis metadata og marker forwarding-resultat uten aa logge payload som standard.",
                fallbackInterests: ["flow", "debug", "diagnostics", "observability", "forwarding", "admin"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: workbenchAccessConfig,
                fallbackSourceCellEndpoint: WorkbenchAccessGrantCell.endpoint,
                fallbackSourceCellName: "WorkbenchAccessGrantCell",
                fallbackPurpose: "Delegert Workbench-tilgang",
                fallbackPurposeDescription: "Utsted og innloes tidsbegrensede invitasjoner som signerer konkrete Workbench-cell agreements.",
                fallbackInterests: ["workbench", "access", "agreement", "delegation", "entity", "dimy"],
                fallbackMenuSlots: [.upperMid, .upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: entityStudioConfig,
                fallbackSourceCellEndpoint: "cell:///EntityStudio",
                fallbackSourceCellName: "EntityStudioCell",
                fallbackPurpose: "Entity browse, redigering og binding-inspeksjon",
                fallbackPurposeDescription: "Utforsk entity-data, signed agreements, agreement refs og binding-ruter i ett arbeidsrom med trygg draft/apply.",
                fallbackInterests: ["entity", "agreements", "binding", "identity", "editing", "inspection", "protocol"],
                fallbackMenuSlots: [.upperLeft, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: participationHubConfig,
                fallbackSourceCellEndpoint: "cell:///ParticipationHub",
                fallbackSourceCellName: "ParticipationHubCell",
                fallbackPurpose: "Invitasjoner og deltakelse paa tvers av workspaces",
                fallbackPurposeDescription: "Bygg og lever generiske workspace-invitasjoner til en Participation Hub, og la mottakers kontekst styre naa eller senere involvering.",
                fallbackInterests: ["participation", "invitation", "collaboration", "chat", "workspace", "agreements"],
                fallbackMenuSlots: [.upperMid, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: conferenceConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceUIRouter",
                fallbackSourceCellName: "ConferenceUIRouterCell",
                fallbackPurpose: "Conference partnering og innsikt",
                fallbackPurposeDescription: "Preview-driven conference MVP med screen map, routing og dispatch via ConferenceUIRouter.",
                fallbackInterests: ["conference", "partnering", "matchmaking", "scheduling", "insights", "routing"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceDemoStoryConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceDemoStory",
                fallbackSourceCellName: "ConferenceDemoStoryCell",
                fallbackPurpose: "Conference demo story orchestration",
                fallbackPurposeDescription: "Start rollebaserte konferansedemohistorier fra Co-Pilot, seed syntetiske demo-brukere via simulation stack og pek videre til eksisterende conference-flater.",
                fallbackInterests: ["conference", "demo", "story", "participant", "sponsor", "exhibitor", "organizer", "simulation", "perspective", "contact-endpoint", "purposeRef=conference.demo.story.run"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: arendalsukaParticipantProgramConfig,
                fallbackSourceCellEndpoint: ArendalsukaConfigurationPublisherContract.endpoint,
                fallbackSourceCellName: "ArendalsukaConfigurationPublisherCell",
                fallbackPurpose: "Arendalsuka participant program",
                fallbackPurposeDescription: "Deltagerflate for vanlige brukere: sok programmet, apne arrangement, finn steder aa motes, oppdag servering/butikker, se kilder og vurder om flaten oppfyller formålene.",
                fallbackInterests: ["arendalsuka", "participant", "program", "ordinary-user", "navigation", "meeting-place", "local-commerce", "democracy", "polling", "provenance", "purposeRef=arendalsuka.participant.good-tool"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: arendalsukaEventAtlasConfig,
                fallbackSourceCellEndpoint: "cell:///ArendalsukaEventAtlas",
                fallbackSourceCellName: "ArendalsukaEventAtlasCell",
                fallbackPurpose: "Arendalsuka event atlas",
                fallbackPurposeDescription: "Importer Arendalsuka-program, klassifiser sesjoner med kildegrunnlag, og koble lokale aktører, tilbud, kartanker, Lost & Found og actor-package entitlements.",
                fallbackInterests: ["arendalsuka", "conference", "program", "agenda", "matching", "local-commerce", "map", "lost-found", "notifications", "actor-packages"],
                fallbackMenuSlots: [.upperMid, .lowerMid, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: conferenceDemoLauncherConfig,
                fallbackSourceCellEndpoint: "cell:///ConfigurationCatalog",
                fallbackSourceCellName: "ConfigurationCatalogCell",
                fallbackPurpose: "Conference demo launcher",
                fallbackPurposeDescription: "Deterministisk startflate som åpner de eksisterende conference-konfigurasjonene i fast demo-rekkefølge uten biblioteksøk eller auth-bypasses.",
                fallbackInterests: ["conference", "demo", "launcher", "participant", "organizer", "web", "binding"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceSkeletonLibraryConfig,
                fallbackSourceCellEndpoint: "cell:///ConfigurationCatalog",
                fallbackSourceCellName: "ConfigurationCatalogCell",
                fallbackPurpose: "Conference skeleton component library",
                fallbackPurposeDescription: "Bla i gjenbrukbare conference-seksjoner, state-keypaths og action-kontrakter som kan brukes av både mennesker og kodeassistenter når nye conference-flater skal bygges.",
                fallbackInterests: ["conference", "skeleton", "components", "design-system", "library", "agent", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceRegistrationSetupConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceOnboarding",
                fallbackSourceCellName: "ConferenceOnboardingCell",
                fallbackPurpose: "Conference registration setup",
                fallbackPurposeDescription: "Cold-start workspace for participant-owned conference registration, profile setup, consent choices, and optional payment prep before entering participantportalen.",
                fallbackInterests: ["conference", "registration", "onboarding", "profile", "consent", "payments", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferencePublicSurfaceConfig,
                fallbackSourceCellEndpoint: "cell:///ConferencePublicShell",
                fallbackSourceCellName: "ConferencePublicShellCell",
                fallbackPurpose: "Conference public website",
                fallbackPurposeDescription: "Public-facing conference shell for landing, tracks, speakers, sessions og publisert praktisk info.",
                fallbackInterests: ["conference", "public", "landing", "tracks", "sessions", "articles", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferencePublicSurfaceClaudeConfig,
                fallbackSourceCellEndpoint: "cell:///ConferencePublicShell",
                fallbackSourceCellName: "ConferencePublicShellCell",
                fallbackPurpose: "Conference public website Claude parity",
                fallbackPurposeDescription: "Claude-designvariant av public-flaten. Den peker til samme ConferencePublicShell data som den eksisterende public-konfigurasjonen, men rendres med warm paper/indigo visual system.",
                fallbackInterests: ["conference", "public", "landing", "claude-design", "visual-parity", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceTrackDetailConfig,
                fallbackSourceCellEndpoint: "cell:///ConferencePublicShell",
                fallbackSourceCellName: "ConferencePublicShellCell",
                fallbackPurpose: "Conference track detail",
                fallbackPurposeDescription: "Detail workspace for the currently selected public conference track before the user enters participant-owned surfaces.",
                fallbackInterests: ["conference", "public", "track-detail", "selection", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceSessionDetailConfig,
                fallbackSourceCellEndpoint: "cell:///ConferencePublicShell",
                fallbackSourceCellName: "ConferencePublicShellCell",
                fallbackPurpose: "Conference session detail",
                fallbackPurposeDescription: "Detail workspace for the currently selected public conference session, with a direct handoff to participant chat and portal.",
                fallbackInterests: ["conference", "public", "session-detail", "selection", "chat", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceAgendaTrackDetailConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
                fallbackSourceCellName: "ConferenceParticipantPreviewShellCell",
                fallbackPurpose: "Conference agenda track detail",
                fallbackPurposeDescription: "Participant-owned detail workspace for the currently selected track in the agenda.",
                fallbackInterests: ["conference", "participant", "agenda", "track-detail", "selection", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceAgendaSessionDetailConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
                fallbackSourceCellName: "ConferenceParticipantPreviewShellCell",
                fallbackPurpose: "Conference agenda session detail",
                fallbackPurposeDescription: "Participant-owned detail workspace for the currently selected session in the agenda.",
                fallbackInterests: ["conference", "participant", "agenda", "session-detail", "selection", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceFeaturedPersonDetailConfig,
                fallbackSourceCellEndpoint: "cell:///ConferencePublicShell",
                fallbackSourceCellName: "ConferencePublicShellCell",
                fallbackPurpose: "Conference featured person detail",
                fallbackPurposeDescription: "Detail workspace for the currently selected featured person in the public conference surface.",
                fallbackInterests: ["conference", "public", "people", "profile", "selection", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceParticipantPortalPreviewConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
                fallbackSourceCellName: "ConferenceParticipantPreviewShellCell",
                fallbackPurpose: "Conference participantportal preview",
                fallbackPurposeDescription: "Full preview-wrapper over participant-shellen for access, onboarding, session thread, polling og shared relations i samme designsystem som dashboardet.",
                fallbackInterests: ["conference", "participant", "preview", "onboarding", "access", "sessions", "polling", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceParticipantPortalConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
                fallbackSourceCellName: "ConferenceParticipantPreviewShellCell",
                fallbackPurpose: "Conference participantportal",
                fallbackPurposeDescription: "Kanonisk participant dashboard over preview-wrapperen til ConferenceParticipantShell, slik at Porthole og Binding leser samme conference-surface.",
                fallbackInterests: ["conference", "participant", "dashboard", "matchmaking", "meetings", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceParticipantPortalClaudeConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
                fallbackSourceCellName: "ConferenceParticipantPreviewShellCell",
                fallbackPurpose: "Conference participantportal Claude parity",
                fallbackPurposeDescription: "Claude-designvariant av participantportalen. Den bruker samme ConferenceParticipantPreviewShell reference som dashboardet, men viser samme data i en lys warm/lavender day-workspace.",
                fallbackInterests: ["conference", "participant", "dashboard", "claude-design", "visual-parity", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceParticipantChatConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceChatLaunch",
                fallbackSourceCellName: "ConferenceChatLaunchCell",
                fallbackPurpose: "Conference participant chat",
                fallbackPurposeDescription: "Eksplisitt chat-workbench for selected-person til chat til follow-up, bygget på den eksisterende ConferenceChatLaunch-cellen.",
                fallbackInterests: ["conference", "participant", "chat", "follow-up", "shared-relations", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceParticipantChatClaudeConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceChatLaunch",
                fallbackSourceCellName: "ConferenceChatLaunchCell",
                fallbackPurpose: "Conference participant chat Claude parity",
                fallbackPurposeDescription: "Claude-designvariant av chatflaten. Den peker til samme ConferenceChatLaunch og participant preview state, men rendres som en mykere proof/chat-opplevelse.",
                fallbackInterests: ["conference", "participant", "chat", "proof", "claude-design", "visual-parity", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceNearbyRadarConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
                fallbackSourceCellName: "ConferenceParticipantPreviewShellCell",
                fallbackPurpose: "Conference nearby radar",
                fallbackPurposeDescription: "Capability-gated nearby workbench over participant discovery. Web stays quiet when scanner capability is absent; Binding can project scanner encounters into the same people rows.",
                fallbackInterests: ["conference", "nearby", "radar", "participant", "scanner", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceNearbyRadarClaudeConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
                fallbackSourceCellName: "ConferenceParticipantPreviewShellCell",
                fallbackPurpose: "Conference nearby radar Claude parity",
                fallbackPurposeDescription: "Claude-designvariant av nearby-flaten. Den peker til samme participant discovery state, men bruker lett blue signal/radar-stil uten aa endre scanner-kontrakten.",
                fallbackInterests: ["conference", "nearby", "radar", "scanner", "claude-design", "visual-parity", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferencePublicProfileEditorConfig,
                fallbackSourceCellEndpoint: "cell:///ConferencePublicProfileEditorPreview",
                fallbackSourceCellName: "ConferencePublicProfileEditorPreviewCell",
                fallbackPurpose: "Conference public profile editor",
                fallbackPurposeDescription: "Deltaker-eid editor for aa velge hvilke profilfelt som eksponeres og hvordan en delbar conference-profil ser ut.",
                fallbackInterests: ["conference", "profile", "participant", "editor", "visibility", "sharing", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferencePublicProfileConfig,
                fallbackSourceCellEndpoint: "cell:///ConferencePublicProfilePreview",
                fallbackSourceCellName: "ConferencePublicProfilePreviewCell",
                fallbackPurpose: "Conference public profile",
                fallbackPurposeDescription: "Viewer-facing conference-profil generert fra deltakerens egne visibility-valg.",
                fallbackInterests: ["conference", "profile", "viewer", "directory", "sharing", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceControlTowerConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceAdminPreviewShell",
                fallbackSourceCellName: "ConferenceAdminPreviewShellCell",
                fallbackPurpose: "Conference control tower",
                fallbackPurposeDescription: "Organizer control tower som samler published content, participant-signaler, KPI-er, simulation og sponsor follow-up i samme demo-flyt som participantportalen.",
                fallbackInterests: ["conference", "organizer", "admin", "control-tower", "insights", "simulation", "publishing", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceControlTowerClaudeConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceAdminPreviewShell",
                fallbackSourceCellName: "ConferenceAdminPreviewShellCell",
                fallbackPurpose: "Conference control tower Claude parity",
                fallbackPurposeDescription: "Claude-designvariant av control tower. Den peker til samme admin preview shell og broadcast studio refs, men rendres med warm paper og amber organizer state.",
                fallbackInterests: ["conference", "organizer", "admin", "control-tower", "claude-design", "visual-parity", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: scaffoldSetupConfig,
                fallbackSourceCellEndpoint: "cell:///ScaffoldSetup",
                fallbackSourceCellName: "ScaffoldSetupCell",
                fallbackPurpose: "Scaffold setup og identity linking",
                fallbackPurposeDescription: "Førstegangsflyt for å bootstrappe scaffold owner og forberede trygg linking mellom web-identitet og Binding-identitet.",
                fallbackInterests: ["scaffold", "setup", "bootstrap", "identity", "linking", "admin", "proofs", "web"],
                fallbackMenuSlots: []
            ),
            scaffoldTemplate(
                configuration: configurationArchitectConfig,
                fallbackSourceCellEndpoint: "cell:///ConfigurationCatalog",
                fallbackSourceCellName: "ConfigurationCatalogCell",
                fallbackPurpose: "CellConfiguration discovery og design",
                fallbackPurposeDescription: "Bruk katalogkontrakter, AI Agent Workspace og Cell Configuration Studio side om side for aa finne eksisterende konfigurasjoner eller utforme komplette nye config-utkast.",
                fallbackInterests: ["configuration", "catalog", "discovery", "ai", "copilot", "skeleton", "library", "binding", "web"],
                fallbackMenuSlots: [.upperLeft, .upperMid]
            ),
            scaffoldTemplate(
                configuration: conferenceAIAssistantConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
                fallbackSourceCellName: "ConferenceParticipantPreviewShellCell",
                fallbackPurpose: "Conference copilot",
                fallbackPurposeDescription: "Konferanse-assistent som kombinerer participant-kontekst med embedded AIGateway for briefing, matchmaking og meeting follow-up.",
                fallbackInterests: ["conference", "ai", "copilot", "participant", "matchmaking", "meetings", "prompting"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: adminControlPlaneOverviewConfig,
                fallbackSourceCellEndpoint: AdminControlPlaneRouting.current.endpoint(for: "AdminOverview"),
                fallbackSourceCellName: "AdminOverviewCell",
                fallbackPurpose: "Admin kontrollplanoversikt",
                fallbackPurposeDescription: "Bekreft releaseidentitet, readiness, datferskhet og nodeflåte før videre rolleavgrenset drift.",
                fallbackInterests: ["admin", "operations", "overview", "readiness", "node-fleet", "purposeRef=admin.scaffold-operations.observe"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: adminOperationsConfig,
                fallbackSourceCellEndpoint: AdminControlPlaneRouting.current.endpoint(for: "AdminHostMetrics"),
                fallbackSourceCellName: "AdminHostMetricsCell",
                fallbackPurpose: "Admin drift",
                fallbackPurposeDescription: "Rolleavgrenset vert-, prosess-, kapasitet-, storage- og deployment-observasjon uten lokal infrastrukturfallback.",
                fallbackInterests: ["admin", "operations", "metrics", "processes", "storage", "deployment", "node-fleet"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: adminSecurityConfig,
                fallbackSourceCellEndpoint: AdminControlPlaneRouting.current.endpoint(for: "AdminSecurityPolicy"),
                fallbackSourceCellName: "AdminSecurityPolicyCell",
                fallbackPurpose: "Admin sikkerhet og tilgang",
                fallbackPurposeDescription: "Revider entry, issuerpolicy, credentials, revokeringer, tilgangsforespørsler og agentnøkler.",
                fallbackInterests: ["admin", "security", "identity", "credentials", "revocation", "access-audit"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: adminProductAdministrationConfig,
                fallbackSourceCellEndpoint: "cell:///ConfigurationCatalog",
                fallbackSourceCellName: "ConfigurationCatalogCell",
                fallbackPurpose: "Produktadministrasjon",
                fallbackPurposeDescription: "Finn produktspesifikke adminflater uten å blande kontrollplan- og produktmyndighet.",
                fallbackInterests: ["admin", "products", "catalog", "conference", "events", "rag"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: adminCopilotConfig,
                fallbackSourceCellEndpoint: AdminControlPlaneRouting.current.endpoint(for: "AdminOverview"),
                fallbackSourceCellName: "AdminOverviewCell",
                fallbackPurpose: "Admin rådgivningsutkast",
                fallbackPurposeDescription: "Lag strukturerte utkast fra eksplisitt redigerte operatørnotater uten automatisk deling av kontrollplandata.",
                fallbackInterests: ["admin", "operations", "ai", "copilot", "handoff", "incident"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: palazzoConciergeConfig,
                fallbackSourceCellEndpoint: "cell:///RestaurantExperiencePlan",
                fallbackSourceCellName: "RestaurantExperiencePlanCell",
                fallbackPurpose: RestaurantPalazzoAIProfile.purpose,
                fallbackPurposeDescription: "Palazzo-orientert hospitalityflate som kombinerer publisert innhold, samtykkebasert gjestekontekst, visit intent og embedded AIGateway i samme arbeidsrom.",
                fallbackInterests: ["restaurant", "hospitality", "concierge", "palazzo", "guest-experience", "ai", "copilot", "oslo"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: palazzoCommunaleConfig,
                fallbackSourceCellEndpoint: PalazzoCommunaleServiceContract.endpoint,
                fallbackSourceCellName: PalazzoCommunaleServiceContract.sourceCellName,
                fallbackPurpose: "Palazzo Communale guest concierge",
                fallbackPurposeDescription: "Kildekontrollert, gjestesikker Palazzo-concierge koblet til PyPalazzoConciergeScaffold gjennom en lokal CellProtocol policy-fasade.",
                fallbackInterests: ["palazzo", "restaurant", "hospitality", "concierge", "guest", "menu", "allergens", "source-citations", "privacy", "web", "binding"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: palazzoGuestConfig,
                fallbackSourceCellEndpoint: "cell:///RestaurantGuestShell",
                fallbackSourceCellName: "RestaurantGuestShellCell",
                fallbackPurpose: "Restaurant guest portal",
                fallbackPurposeDescription: "Guest-owned Palazzo-shell for purpose, consent, visit planning, and AI-assisted experience preparation.",
                fallbackInterests: ["restaurant", "guest", "hospitality", "concierge", "palazzo", "visit-planning", "web", "binding"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: palazzoStaffConfig,
                fallbackSourceCellEndpoint: "cell:///RestaurantStaffShell",
                fallbackSourceCellName: "RestaurantStaffShellCell",
                fallbackPurpose: "Restaurant staff console",
                fallbackPurposeDescription: "Staff-facing Palazzo-shell for consent-aware guest context, service readiness, and staff brief publication.",
                fallbackInterests: ["restaurant", "staff", "hospitality", "concierge", "palazzo", "service", "web", "binding"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: conferenceBroadcastStudioConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceBroadcastStudio",
                fallbackSourceCellName: "ConferenceBroadcastStudioCell",
                fallbackPurpose: "Organizer-broadcast og notification testing",
                fallbackPurposeDescription: "Bygg og test conference-broadcasts mot registrerte enheter, med synlig filtrering for abonnement, mute og conference-scope.",
                fallbackInterests: ["conference", "organizer", "notifications", "broadcast", "devices", "testing"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: conferenceSponsorConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceSponsorPreviewShell",
                fallbackSourceCellName: "ConferenceSponsorPreviewShellCell",
                fallbackPurpose: "Conference sponsor follow-up",
                fallbackPurposeDescription: "Preview-wrapper over sponsor follow-up, slik at Porthole og web kan bruke samme skeleton mens Binding fortsatt kan resolve direkte sponsor-identitet når det trengs.",
                fallbackInterests: ["conference", "sponsor", "lead-vault", "consent", "follow-up", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: conferenceSponsorClaudeConfig,
                fallbackSourceCellEndpoint: "cell:///ConferenceSponsorPreviewShell",
                fallbackSourceCellName: "ConferenceSponsorPreviewShellCell",
                fallbackPurpose: "Conference sponsor follow-up Claude parity",
                fallbackPurposeDescription: "Claude-designvariant av sponsor follow-up. Den peker til samme sponsor preview shell, men rendres som green consent pipeline.",
                fallbackInterests: ["conference", "sponsor", "lead-vault", "consent", "claude-design", "visual-parity", "binding", "web"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: eventPublisherOnboardingConfig,
                fallbackSourceCellEndpoint: "cell:///EventPublisherOnboarding",
                fallbackSourceCellName: "EventPublisherOnboardingCell",
                fallbackPurpose: "Event publisher onboarding",
                fallbackPurposeDescription: "Self-service onboarding for aktorer som vil opprette sin egen profil, teamrollemodell og starte publisering av flere eventer.",
                fallbackInterests: ["events", "publisher", "onboarding", "directory", "admin", "multi-tenant"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: eventDirectoryConfig,
                fallbackSourceCellEndpoint: "cell:///EventDirectoryAggregator",
                fallbackSourceCellName: "EventDirectoryAggregatorCell",
                fallbackPurpose: "Global event discovery",
                fallbackPurposeDescription: "DiMy-hostet katalog for publiserte eventer og aktorer med lokalt speilet offentlig indeks og opt-in federert sok.",
                fallbackInterests: ["events", "directory", "search", "public", "discovery", "federation"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: eventPublisherAdminConfig,
                fallbackSourceCellEndpoint: "cell:///EventPublisherAdminShell",
                fallbackSourceCellName: "EventPublisherAdminShellCell",
                fallbackPurpose: "Publisher admin workspace",
                fallbackPurposeDescription: "Adminflate for aktorprofil, teamroller, federation policy og opprettelse av flere eventer under samme publisher.",
                fallbackInterests: ["events", "publisher", "admin", "roles", "federation", "directory"],
                fallbackMenuSlots: [.upperMid, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: eventActorDirectoryConfig,
                fallbackSourceCellEndpoint: "cell:///EventActorDirectory",
                fallbackSourceCellName: "EventActorDirectoryCell",
                fallbackPurpose: "Actor event directory",
                fallbackPurposeDescription: "Offentlig aktorside som eksponerer publisher-profil, publiserte eventkort og federation capability for en enkelt aktor.",
                fallbackInterests: ["events", "actor", "directory", "public", "listing", "publisher"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: eventPublicSurfaceConfig,
                fallbackSourceCellEndpoint: "cell:///EventPublicShell",
                fallbackSourceCellName: "EventPublicShellCell",
                fallbackPurpose: "Event public surface",
                fallbackPurposeDescription: "Oppdagelsesdrevet offentlig eventflate med tidspunkt, sted, tags og CTA, og mulighet for template-spesifikk handoff ved behov.",
                fallbackInterests: ["events", "public", "landing", "directory", "cta", "discovery"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: eventAdminWorkspaceConfig,
                fallbackSourceCellEndpoint: "cell:///EventAdminShell",
                fallbackSourceCellName: "EventAdminShellCell",
                fallbackPurpose: "Event admin workspace",
                fallbackPurposeDescription: "Rediger, publiser og arkiver ett event med generisk lifecycle-stotte for conference, meetup eller andre templates.",
                fallbackInterests: ["events", "admin", "publish", "metadata", "cta", "workflow"],
                fallbackMenuSlots: [.upperMid, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: eventFederationSearchConfig,
                fallbackSourceCellEndpoint: "cell:///EventFederationBroker",
                fallbackSourceCellName: "EventFederationBrokerCell",
                fallbackPurpose: "Federated event search inspection",
                fallbackPurposeDescription: "Inspeksjonsflate for query expansion mot aktorer som har opt-in pa federert offentlig sok, uten aa lage en parallell sannhet utenfor cells.",
                fallbackInterests: ["events", "federation", "search", "public", "broker", "query-expansion"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: aiGatewayConfig,
                fallbackSourceCellEndpoint: "cell:///AIGateway",
                fallbackSourceCellName: "AIGatewayCell",
                fallbackPurpose: "AI agent og modellgateway",
                fallbackPurposeDescription: "Embeddable agentflate for prompt, modellvalg og setup-aware API/BYOK-flyt.",
                fallbackInterests: ["ai", "agent", "llm", "gateway", "byok", "prompting", "guided-setup", "purposeRef=personal.ai.gateway.configure"],
                fallbackMenuSlots: [.upperLeft, .upperMid]
            ),
            scaffoldTemplate(
                configuration: ragConfig,
                fallbackSourceCellEndpoint: "cell:///RAGGateway",
                fallbackSourceCellName: "RAGGatewayCell",
                fallbackPurpose: "Domenespesifikk RAG-utforskning",
                fallbackPurposeDescription: "Case-aware RAG for sporsmal, sitater, corpus-utforskning og dokumentlenker.",
                fallbackInterests: ["rag", "documentation", "prompts", "knowledge", "citations", "search"],
                fallbackMenuSlots: [.upperLeft, .upperMid]
            ),
            scaffoldTemplate(
                configuration: ragPromptAdminConfig,
                fallbackSourceCellEndpoint: "cell:///RAGPromptAdmin",
                fallbackSourceCellName: "RAGPromptAdminCell",
                fallbackPurpose: "RAG promptadministrasjon",
                fallbackPurposeDescription: "Se aktive promptprofiler, styr runtime override og deleger promptadmin for RAG-instansen.",
                fallbackInterests: ["rag", "prompts", "admin", "configuration", "operations"],
                fallbackMenuSlots: [.upperMid, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: innoragPromptAdminConfig,
                fallbackSourceCellEndpoint: "cell:///RAGPromptAdmin",
                fallbackSourceCellName: "RAGPromptAdminCell",
                fallbackPurpose: "Innorag promptadministrasjon",
                fallbackPurposeDescription: "Se aktive promptprofiler, styr runtime override og deleger promptadmin for innovasjons-RAG-en.",
                fallbackInterests: ["rag", "innovasjon", "prompts", "admin", "configuration", "operations"],
                fallbackMenuSlots: [.upperMid, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: docPromptAdminConfig,
                fallbackSourceCellEndpoint: "cell:///RAGPromptAdmin",
                fallbackSourceCellName: "RAGPromptAdminCell",
                fallbackPurpose: "Dokumentasjons-RAG promptadministrasjon",
                fallbackPurposeDescription: "Se aktive promptprofiler, styr runtime override og deleger promptadmin for dokumentasjons-RAG-en.",
                fallbackInterests: ["rag", "documentation", "prompts", "admin", "configuration", "operations"],
                fallbackMenuSlots: [.upperMid, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: todoConfig,
                fallbackSourceCellEndpoint: "cell:///Todo",
                fallbackSourceCellName: "TodoCell",
                fallbackPurpose: "Personlig todo-liste",
                fallbackPurposeDescription: "Today/Important/Recurring/Inbox-oppsett med frister, prioritet, etiketter, delsteg og gjentakelser.",
                fallbackInterests: ["todo", "tasks", "planning", "priority", "tags", "recurring", "personal-productivity"],
                fallbackMenuSlots: [.lowerMid, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: todoPlannerConfig,
                fallbackSourceCellEndpoint: "cell:///Todo",
                fallbackSourceCellName: "TodoCell",
                fallbackPurpose: "Todo planner copilot",
                fallbackPurposeDescription: "Planleggingsflate som kombinerer personlige todo-lister med embedded AIGateway for prioritering, ukesplan og neste steg.",
                fallbackInterests: ["todo", "planning", "ai", "copilot", "priority", "weekly-review", "personal-productivity"],
                fallbackMenuSlots: [.lowerMid, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: ideaTaskShareConfig,
                fallbackSourceCellEndpoint: "cell:///IdeaTaskShare",
                fallbackSourceCellName: "IdeaTaskShareCell",
                fallbackPurpose: "Delt idesnapshot",
                fallbackPurposeDescription: "Read-only delt snapshot av valgt ide og relaterte todoer, publisert fra personlig workspace og oppdatert via share-feed.",
                fallbackInterests: ["ideas", "todo", "sharing", "snapshot", "review", "cellprotocol"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: ideaTaskWorkspaceConfig,
                fallbackSourceCellEndpoint: "cell:///IdeaTaskWorkspace",
                fallbackSourceCellName: "IdeaTaskWorkspaceCell",
                fallbackPurpose: "Idé til handling",
                fallbackPurposeDescription: "Personlig workspace som gjør en løs idé om til ett konkret neste steg med Vault som idé-lager og Todo som oppgavelager.",
                fallbackInterests: ["ideas", "todo", "vault", "planning", "next-step", "personal-productivity", "cellprotocol"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: havenWorkbenchConfig,
                fallbackSourceCellEndpoint: "cell:///WorkItem",
                fallbackSourceCellName: "WorkItemCell",
                fallbackPurpose: "HAVEN project workbench",
                fallbackPurposeDescription: "Samlet V0.5-flate for canonical work items, ideinntak, triage, backlog, portfolio, roadmap, graf, GitHub-sync og docs.",
                fallbackInterests: ["haven", "projects", "tasks", "bugs", "features", "triage", "roadmap", "portfolio", "graph", "github", "docs", "board", "kanban", "trello", "purposeRef=haven.work.board.view"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: workItemConfig,
                fallbackSourceCellEndpoint: "cell:///WorkItem",
                fallbackSourceCellName: "WorkItemCell",
                fallbackPurpose: "Canonical HAVEN work items",
                fallbackPurposeDescription: "Fang og triager ideer, features, bugs, docs, research, beslutninger og implementation gaps med evidens og neste handling.",
                fallbackInterests: ["haven", "work-items", "bugs", "features", "triage", "backlog", "implementation-gaps"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: projectPortfolioConfig,
                fallbackSourceCellEndpoint: "cell:///ProjectPortfolio",
                fallbackSourceCellName: "ProjectPortfolioCell",
                fallbackPurpose: "Canonical HAVEN project portfolio",
                fallbackPurposeDescription: "Hold prosjektstatus, helse, prioritet, releases, capacity, saved views, repo-/celleref og lenker til WorkItem.",
                fallbackInterests: ["haven", "projects", "portfolio", "roadmap", "health", "planning", "work-items", "releases", "capacity", "saved-views"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: githubWorkSyncConfig,
                fallbackSourceCellEndpoint: "cell:///GitHubWorkSync",
                fallbackSourceCellName: "GitHubWorkSyncCell",
                fallbackPurpose: "GitHub work sync",
                fallbackPurposeDescription: "Importer GitHub issue/PR-fixtures til WorkItem-payloads og ko ekstern write-back eksplisitt, uten automatisk nettverksskriving.",
                fallbackInterests: ["haven", "github", "issues", "pull-requests", "work-items", "sync", "ci"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: cellOwnershipMapConfig,
                fallbackSourceCellEndpoint: "cell:///EntityCellGraph",
                fallbackSourceCellName: "EntityCellGraphCell",
                fallbackPurpose: "Cell ownership/access map",
                fallbackPurposeDescription: "Obsidian-lignende graf over celler requesteren eier, har tilgang til, kjører lokalt, er persistente eller kjenner som remote routes.",
                fallbackInterests: ["cellprotocol", "cells", "ownership", "access", "identity", "graph", "scaffold", "remote", "purposeRef=cell.access.graph.view"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: mermaidConfig,
                fallbackSourceCellEndpoint: "cell:///MermaidRenderer",
                fallbackSourceCellName: "MermaidRendererCell",
                fallbackPurpose: "Mermaid diagram-rendering",
                fallbackPurposeDescription: "Render Mermaid-diagrammer med webview-backend (SVG/PNG) og native backend (PNG der støttet).",
                fallbackInterests: ["mermaid", "diagram", "flowchart", "rendering", "svg", "png", "deterministic", "resource-router", "purposeRef=personal.diagram.mermaid.render"],
                fallbackMenuSlots: [.upperLeft, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: conferenceOwnershipConfig,
                fallbackSourceCellEndpoint: "cell:///MarkdownRenderer",
                fallbackSourceCellName: "MarkdownRendererCell",
                fallbackPurpose: "Konferanse ownership- og dataflytdiagram",
                fallbackPurposeDescription: "Render den kanoniske bokdokumentasjonen for conference ownership/dataflow med Mermaid delegert til MermaidRenderer.",
                fallbackInterests: ["conference", "ownership", "dataflow", "documentation", "mermaid", "access"],
                fallbackMenuSlots: [.upperLeft, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: vaultStudioConfig,
                fallbackSourceCellEndpoint: "cell:///VaultStudio",
                fallbackSourceCellName: "VaultStudioWorkspaceCell",
                fallbackPurpose: "CellProtocol-native knowledge workspace",
                fallbackPurposeDescription: "Arbeidsflate for notater, prosjekter, referanser, AI-stotte og grafprojeksjon bygget rundt vault.state snapshots og live Flow-events.",
                fallbackInterests: ["vault", "studio", "knowledge-graph", "markdown", "ai", "cellprotocol", "mermaid"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: projectOperationsConfig,
                fallbackSourceCellEndpoint: "cell:///ServiceCatalog",
                fallbackSourceCellName: "ServiceCatalogCell",
                fallbackPurpose: "Project operations og servicekatalog",
                fallbackPurposeDescription: "Intern arbeidsflate for servicekatalog, RAG query, promptbibliotek, generiske drafts/versions og ærlig implementation queue.",
                fallbackInterests: ["project-operations", "service-catalog", "rag", "drafts", "versions", "prompts", "implementation-queue"],
                fallbackMenuSlots: [.upperLeft, .upperMid]
            ),
            scaffoldTemplate(
                configuration: vaultConfig,
                fallbackSourceCellEndpoint: "cell:///Vault",
                fallbackSourceCellName: "VaultCell",
                fallbackPurpose: "Notatgraf (Obsidian-stil)",
                fallbackPurposeDescription: "Opprett/list notater og koblinger via vault.note.* / vault.link.add for Obsidian-lignende arbeidsflyt.",
                fallbackInterests: ["vault", "notes", "obsidian", "knowledge-graph", "markdown"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: obsidianAIConfig,
                fallbackSourceCellEndpoint: "cell:///Vault",
                fallbackSourceCellName: "VaultCell",
                fallbackPurpose: "Obsidian copilot",
                fallbackPurposeDescription: "Kombiner Vault-noteoperasjoner med embedded AIGateway for sammendrag, strukturering og neste steg i samme arbeidsflate.",
                fallbackInterests: ["vault", "obsidian", "ai", "copilot", "notes", "knowledge-graph", "markdown"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: stagingDemoConfig,
                fallbackSourceCellEndpoint: "cell:///Vault",
                fallbackSourceCellName: "VaultCell",
                fallbackPurpose: "Staging demo for Vault og Mermaid",
                fallbackPurposeDescription: "Kombinert notat- og diagramarbeidsflate som viser hvordan flere cellereferanser kan brukes i én web-klar konfigurasjon.",
                fallbackInterests: ["staging", "vault", "obsidian", "mermaid", "diagram", "demo"],
                fallbackMenuSlots: [.upperLeft, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: catalogConfig,
                fallbackSourceCellEndpoint: "cell:///ConfigurationCatalog",
                fallbackSourceCellName: "ConfigurationCatalogCell",
                fallbackPurpose: "Konfigurasjonskatalog og discovery",
                fallbackPurposeDescription: "Publiserer konfigurasjoner, menyer og matching slik at Binding kan discovere resten av scaffoldet.",
                fallbackInterests: ["catalog", "configuration", "discovery", "binding", "menus", "matching"],
                fallbackMenuSlots: [.upperRight, .lowerLeft]
            ),
            scaffoldTemplate(
                configuration: consentReceiptConfig,
                fallbackSourceCellEndpoint: "cell:///ConsentReceipt",
                fallbackSourceCellName: "ConsentReceiptCell",
                fallbackPurpose: "Samtykkekvitteringer og receipts",
                fallbackPurposeDescription: "Se og bruk lagrede consent receipts som del av lead- og agreement-flyt.",
                fallbackInterests: ["consent", "receipts", "conference", "audit", "lead-vault"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: exhibitorAccessConfig,
                fallbackSourceCellEndpoint: "cell:///ExhibitorAccess",
                fallbackSourceCellName: "ExhibitorAccessCell",
                fallbackPurpose: "Exhibitor-tilgang og entitlement",
                fallbackPurposeDescription: "Vis og bruk exhibitor-access state som del av lead- og conference-flyt.",
                fallbackInterests: ["conference", "exhibitor", "access", "entitlements", "lead-vault"],
                fallbackMenuSlots: [.upperMid, .lowerMid]
            ),
            scaffoldTemplate(
                configuration: deviceRegistrationConfig,
                fallbackSourceCellEndpoint: "cell:///DeviceRegistration",
                fallbackSourceCellName: "DeviceRegistrationCell",
                fallbackPurpose: "Enhetsregistrering for callbacks",
                fallbackPurposeDescription: "Følg registrerte enheter og callback-klare klienter i conference-notification-flyt.",
                fallbackInterests: ["conference", "devices", "callbacks", "notifications", "registration"],
                fallbackMenuSlots: [.upperRight, .lowerRight]
            ),
            scaffoldTemplate(
                configuration: paymentGateConfig,
                fallbackSourceCellEndpoint: "cell:///PaymentGate",
                fallbackSourceCellName: "PaymentGateCell",
                fallbackPurpose: "Micropayment-gating og receipts",
                fallbackPurposeDescription: "Quote, receipt og adgangsgating for ressurser som krever betaling eller prepaid saldo.",
                fallbackInterests: ["payments", "micropayments", "receipts", "access", "commerce"],
                fallbackMenuSlots: [.lowerRight]
            ),
            scaffoldTemplate(
                configuration: paymentProofDoorConfig,
                fallbackSourceCellEndpoint: "cell:///PaymentProofDoor",
                fallbackSourceCellName: "PaymentProofDoorCell",
                fallbackPurpose: "Proof-gated adgang",
                fallbackPurposeDescription: "Vis og juster proof-kravet som kreves for å komme gjennom en betalingsstyrt door.",
                fallbackInterests: ["payments", "proofs", "entitlements", "agreements", "access"],
                fallbackMenuSlots: [.lowerRight]
            ),
            scaffoldTemplate(
                configuration: smiAgreementSettlementConfig,
                fallbackSourceCellEndpoint: "cell:///SMIAgreementSettlement",
                fallbackSourceCellName: "SMIAgreementSettlementCell",
                fallbackPurpose: "SMI agreement settlement sidecar",
                fallbackPurposeDescription: "Sidecar for transparente SMI-vilkår, settlement-instruksjoner, ressurskost, evidence og audit.",
                fallbackInterests: ["somebodymakeit", "agreement", "settlement", "conditions", "value-flow", "audit"],
                fallbackMenuSlots: [.upperMid, .lowerRight]
            )
        ]

        templates.append(contentsOf: skeletonParityConfigs.map { configuration in
            scaffoldTemplate(
                configuration: configuration,
                fallbackSourceCellEndpoint: configuration.discovery?.sourceCellEndpoint ?? "cell:///Unknown",
                fallbackSourceCellName: configuration.discovery?.sourceCellName ?? configuration.name,
                fallbackPurpose: configuration.discovery?.purpose ?? configuration.name,
                fallbackPurposeDescription: configuration.discovery?.purposeDescription
                    ?? configuration.description
                    ?? "Deterministisk scaffold-eid parity-fixture for Binding og web renderer-sammenligning.",
                fallbackInterests: configuration.discovery?.interests ?? ["skeleton", "parity", "binding", "renderer"],
                fallbackMenuSlots: []
            )
        })
        templates.append(contentsOf: webKnowledgeConfigs.map { configuration in
            scaffoldTemplate(
                configuration: configuration,
                fallbackSourceCellEndpoint: configuration.discovery?.sourceCellEndpoint ?? "cell:///Unknown",
                fallbackSourceCellName: configuration.discovery?.sourceCellName ?? configuration.name,
                fallbackPurpose: configuration.discovery?.purpose ?? configuration.name,
                fallbackPurposeDescription: configuration.discovery?.purposeDescription
                    ?? configuration.description
                    ?? "Requester-scoped knowledge and truth-source tooling for Co-Pilot and Porthole.",
                fallbackInterests: configuration.discovery?.interests ?? ["knowledge", "truth-source", "web", "credentials"],
                fallbackMenuSlots: []
            )
        })
        templates.append(contentsOf: transcriptConfigs.map { configuration in
            scaffoldTemplate(
                configuration: configuration,
                fallbackSourceCellEndpoint: configuration.discovery?.sourceCellEndpoint ?? TranscriptStoreContract.endpoint,
                fallbackSourceCellName: configuration.discovery?.sourceCellName ?? configuration.name,
                fallbackPurpose: configuration.discovery?.purpose ?? configuration.name,
                fallbackPurposeDescription: configuration.discovery?.purposeDescription
                    ?? configuration.description
                    ?? "Requester-scoped retention-governed storage for verbatim material.",
                fallbackInterests: configuration.discovery?.interests ?? ["transcript", "evidence", "retention-governed"],
                fallbackMenuSlots: []
            )
        })
        templates.append(contentsOf: spatialConfigs.map { configuration in
            scaffoldTemplate(
                configuration: configuration,
                fallbackSourceCellEndpoint: configuration.discovery?.sourceCellEndpoint ?? "cell:///SpatialProjection",
                fallbackSourceCellName: configuration.discovery?.sourceCellName ?? "SpatialProjectionCell",
                fallbackPurpose: configuration.discovery?.purpose ?? "Purpose-filtered map",
                fallbackPurposeDescription: configuration.discovery?.purposeDescription
                    ?? configuration.description
                    ?? "Requester-visible map surface for spatial data, nearby artifacts and explicit presence sharing.",
                fallbackInterests: configuration.discovery?.interests ?? ["map", "spatial", "nearby", "location"],
                fallbackMenuSlots: []
            )
        })
        templates.append(contentsOf: personalCopilotConfigs.map { configuration in
            scaffoldTemplate(
                configuration: configuration,
                fallbackSourceCellEndpoint: configuration.discovery?.sourceCellEndpoint ?? "cell:///Unknown",
                fallbackSourceCellName: configuration.discovery?.sourceCellName ?? configuration.name,
                fallbackPurpose: configuration.discovery?.purpose ?? configuration.name,
                fallbackPurposeDescription: configuration.discovery?.purposeDescription
                    ?? configuration.description
                    ?? "Personal Co-Pilot V1 surface for Binding and Porthole runtime iteration.",
                fallbackInterests: configuration.discovery?.interests ?? ["personal-copilot-v1", "binding"],
                fallbackMenuSlots: []
            )
        })
        templates.append(contentsOf: personalEntityActivityConfigs.map { configuration in
            scaffoldTemplate(
                configuration: configuration,
                fallbackSourceCellEndpoint: configuration.discovery?.sourceCellEndpoint ?? "cell:///Unknown",
                fallbackSourceCellName: configuration.discovery?.sourceCellName ?? configuration.name,
                fallbackPurpose: configuration.discovery?.purpose ?? "Eierens gjeldende arbeids- og prosjektstatus",
                fallbackPurposeDescription: configuration.discovery?.purposeDescription
                    ?? configuration.description
                    ?? "Read-only owner overview over requester-authorized work and project state.",
                fallbackInterests: configuration.discovery?.interests ?? ["activity", "dashboard", "owner", "projects", "work-items"],
                fallbackMenuSlots: []
            )
        })

        return templates
    }

    private static func scaffoldTemplate(
        configuration: CellConfiguration,
        fallbackSourceCellEndpoint: String,
        fallbackSourceCellName: String,
        fallbackPurpose: String,
        fallbackPurposeDescription: String,
        fallbackInterests: [String],
        fallbackMenuSlots: [MenuSlot]
    ) -> ScaffoldPurposeTemplate {
        let discovery = configuration.discovery
        let sourceCellEndpoint = discovery?.sourceCellEndpoint ?? fallbackSourceCellEndpoint
        let sourceCellName = discovery?.sourceCellName ?? fallbackSourceCellName
        let purpose = discovery?.purpose ?? fallbackPurpose
        let purposeDescription = discovery?.purposeDescription ?? fallbackPurposeDescription
        let interests = discovery?.interests.isEmpty == false ? discovery?.interests ?? fallbackInterests : fallbackInterests
        let menuSlots = discovery?.menuSlots.compactMap(MenuSlot.init(rawValue:)) ?? []

        return ScaffoldPurposeTemplate(
            sourceCellEndpoint: sourceCellEndpoint,
            sourceCellName: sourceCellName,
            purpose: purpose,
            purposeDescription: purposeDescription,
            interests: interests,
            menuSlots: menuSlots.isEmpty ? fallbackMenuSlots : menuSlots,
            goal: configuration,
            configuration: configuration
        )
    }

    static func defaultCatalogConfigurations() -> [CellConfiguration] {
        scaffoldPurposeTemplates().map(\.configuration)
    }

    static func defaultCatalogConfigurations(forMenuKeypath keypath: String) -> [CellConfiguration] {
        guard let slot = MenuSlot.allCases.first(where: { $0.keypath == keypath }) else {
            return []
        }

        return scaffoldPurposeTemplates()
            .filter { $0.menuSlots.contains(slot) }
            .map(\.configuration)
    }

    private static func objectValue<T: Encodable>(from value: T) -> Object {
        guard let data = try? JSONEncoder().encode(value),
              let decoded = try? JSONDecoder().decode(ValueType.self, from: data),
              case let .object(object) = decoded else {
            return [:]
        }
        return object
    }

    static func portholePublishedConfigurations(from configurations: [CellConfiguration]) -> [CellConfiguration] {
        var seen = Set<String>()
        var filtered = [CellConfiguration]()

        for configuration in configurations {
            guard isPortholePublishedConfiguration(configuration) else {
                continue
            }

            let identity = portholeConfigurationIdentity(for: configuration)
            if seen.insert(identity).inserted {
                filtered.append(configuration)
            }
        }

        return filtered.sorted(by: comparePortholePublishedConfigurations)
    }

    /// Returns the catalog templates that are safe to publish from the
    /// scaffold-owned, read-only catalog projection. This deliberately does
    /// not reuse requester-specific catalog state: overlays, private
    /// workbenches, admin surfaces and agreement-gated event configurations
    /// must never become public merely because the catalog endpoint is public.
    static func ownerPublishedReadConfigurations(
        from configurations: [CellConfiguration]
    ) -> [CellConfiguration] {
        portholePublishedConfigurations(from: configurations)
            .filter(isOwnerPublishedReadConfiguration)
            .map(sanitizedOwnerPublishedReadConfiguration)
    }

    static func isOwnerPublishedReadConfiguration(_ configuration: CellConfiguration) -> Bool {
        guard isPortholePublishedConfiguration(configuration),
              isRemoteEventConfiguration(configuration) == false,
              isSharedWorkbenchConfiguration(configuration) == false,
              let endpoint = normalizedPortholeEndpoint(for: configuration) else {
            return false
        }

        let normalizedEndpoint = endpoint.lowercased()
        if ownerPublishedReadDeniedEndpointTokens.contains(where: normalizedEndpoint.contains) {
            return false
        }

        var policyComponents = [String]()
        policyComponents.append(configuration.name)
        policyComponents.append(configuration.description ?? "")
        policyComponents.append(configuration.discovery?.purpose ?? "")
        policyComponents.append(configuration.discovery?.purposeDescription ?? "")
        policyComponents.append(contentsOf: configuration.discovery?.interests ?? [])
        let policyTerms = policyComponents
            .joined(separator: " ")
            .folding(options: [.caseInsensitive, .diacriticInsensitive], locale: .current)
            .lowercased()
        let policyWords = Set(policyTerms.split { character in
            character.isLetter == false && character.isNumber == false
        }.map(String.init))

        return policyWords.isDisjoint(with: ownerPublishedReadDeniedPolicyTerms)
    }

    private static let ownerPublishedReadDeniedEndpointTokens: [String] = [
        "admin",
        "agreementworkbench",
        "cellconfigurationstudio",
        "configurationcatalog",
        "draftversion",
        "entitystudio",
        "flowdebugprobe",
        "githubworksync",
        "ideatask",
        "projectportfolio",
        "ragcatalogingestion",
        "ragingestmedia",
        "ragpromptadmin",
        "scaffoldsetup",
        "securityworkbench",
        "servicecatalog",
        "softwaredistribution",
        "trustpacket",
        "vault",
        "workbenchaccessgrant",
        "workitem"
    ]

    private static let ownerPublishedReadDeniedPolicyTerms: Set<String> = [
        "admin",
        "administrator",
        "operator",
        "private",
        "privat"
    ]

    private static func isRemoteEventConfiguration(_ configuration: CellConfiguration) -> Bool {
        remoteEventConfigurationAccessRequirements.contains { requirement in
            configuration.discovery?.sourceCellEndpoint == requirement.sourceCellEndpoint
                || configuration.cellReferences?.contains(where: { $0.endpoint == requirement.sourceCellEndpoint }) == true
                || configuration.name == requirement.configurationName
        }
    }

    private static func sanitizedOwnerPublishedReadConfiguration(
        _ configuration: CellConfiguration
    ) -> CellConfiguration {
        var sanitized = configuration
        sanitized.cellReferences = configuration.cellReferences?.map(sanitizedOwnerPublishedReadReference)
        return sanitized
    }

    private static func sanitizedOwnerPublishedReadReference(_ reference: CellReference) -> CellReference {
        var sanitized = reference
        // Loading a public catalog row is discovery, not authorization to run
        // initialization writes or to subscribe the remote runtime to feeds.
        sanitized.setKeysAndValues = []
        sanitized.subscribeFeed = false
        sanitized.subscriptions = []
        return sanitized
    }

    static func isPortholePublishedConfiguration(_ configuration: CellConfiguration) -> Bool {
        let hasRenderableBody = configuration.skeleton != nil
            || configuration.cellReferences?.isEmpty == false
        guard hasRenderableBody else {
            return false
        }

        if isSharedWorkbenchConfiguration(configuration) {
            return true
        }

        guard let endpoint = normalizedPortholeEndpoint(for: configuration) else {
            return false
        }

        let publishedControlPlaneNames: Set<String> = [
            AdminWorkspaceConfigurationFactory.overviewName,
            AdminWorkspaceConfigurationFactory.operationsName,
            AdminWorkspaceConfigurationFactory.securityName,
            AdminWorkspaceConfigurationFactory.copilotName
        ]
        let adminRouting = AdminControlPlaneRouting.current
        let isControlPlaneEndpoint = AdminScaffoldPublishedSurfacePolicy.allowedCellNames.contains { cellName in
            endpoint == adminRouting.endpoint(for: cellName)
        }
        if isControlPlaneEndpoint {
            return publishedControlPlaneNames.contains(configuration.name)
        }
        return portholeSupportedEndpoints.contains(endpoint)
    }

    private static func isSharedWorkbenchConfiguration(_ configuration: CellConfiguration) -> Bool {
        let discoveryEndpoint = configuration.discovery?.sourceCellEndpoint?
            .trimmingCharacters(in: .whitespacesAndNewlines)
        let hasConcreteOwnerDiscoveryEndpoint = discoveryEndpoint?.hasPrefix("cell:///") == true
            && discoveryEndpoint != "cell:///WorkItem"

        return configuration.name == WorkbenchAccessGrantCell.sharedWorkbenchConfigurationName
            && configuration.uuid.hasPrefix("shared-workbench-")
            && configuration.discovery?.sourceCellName == "WorkItemCell"
            && hasConcreteOwnerDiscoveryEndpoint
            && configuration.cellReferences?.contains { reference in
                guard reference.label == "workItems" else {
                    return false
                }
                let endpoint = reference.endpoint.trimmingCharacters(in: .whitespacesAndNewlines)
                return endpoint == "cell:///WorkItem"
                    || endpoint == WorkbenchAccessGrantCell.sharedWorkbenchConcreteEndpoint(
                        in: configuration,
                        label: "workItems",
                        sourceEndpoint: nil
                    )
            } == true
    }

    private static func normalizedPortholeEndpoint(for configuration: CellConfiguration) -> String? {
        let rawEndpoint = configuration.discovery?.sourceCellEndpoint
            ?? configuration.cellReferences?.first?.endpoint
        guard let rawEndpoint else {
            return nil
        }

        let trimmed = rawEndpoint.trimmingCharacters(in: .whitespacesAndNewlines)
        guard trimmed.isEmpty == false else {
            return nil
        }

        return trimmed
    }

    private static func comparePortholePublishedConfigurations(_ lhs: CellConfiguration, _ rhs: CellConfiguration) -> Bool {
        let lhsPriority = conferencePortholePriority(for: lhs)
        let rhsPriority = conferencePortholePriority(for: rhs)

        if lhsPriority != rhsPriority {
            return lhsPriority < rhsPriority
        }

        return lhs.name.localizedCaseInsensitiveCompare(rhs.name) == .orderedAscending
    }

    private static func conferencePortholePriority(for configuration: CellConfiguration) -> Int {
        conferencePortholePriorityByName[configuration.name] ?? Int.max
    }

    private static func portholeConfigurationIdentity(for configuration: CellConfiguration) -> String {
        let endpoint = normalizedPortholeEndpoint(for: configuration) ?? ""
        return "\(endpoint.lowercased())::\(configuration.name.lowercased())"
    }

    static func mermaidRendererConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Mermaid Renderer Playground")
        configuration.description = "Mermaid playground med fri tekst-input, deterministiske preset-kall og state-visning av siste render-respons."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///MermaidRenderer",
            sourceCellName: "MermaidRendererCell",
            purpose: "Mermaid diagram-rendering",
            purposeDescription: "Render Mermaid-diagrammer med webview-backend (SVG/PNG) og native backend (PNG der støttet).",
            interests: ["mermaid", "diagram", "flowchart", "rendering", "svg", "png", "deterministic", "resource-router", "purposeRef=personal.diagram.mermaid.render"],
            menuSlots: ["upperLeft", "lowerLeft"]
        )

        let reference = CellReference(endpoint: "cell:///MermaidRenderer", label: "mermaidRenderer")
        configuration.addReference(reference)

        var elements = SkeletonElementList()
        elements.append(catalogText("Mermaid Renderer Playground"))
        elements.append(catalogText("Rediger kilde, bruk Cmd/Ctrl+Enter for standard SVG-render, eller kjør preset-kall for webview/native backend. State-seksjonen under viser siste respons og cache/runtime-status."))
        elements.append(contentsOf: mermaidRendererSections(
            referenceLabel: "mermaidRenderer",
            sampleSource: mermaidPlaygroundSampleSource,
            svgPayload: mermaidWebViewSVGPayload(
                source: mermaidPlaygroundSampleSource,
                correlationId: "catalog-webview-svg"
            ),
            pngPayload: mermaidWebViewPNGPayload(
                source: mermaidPlaygroundSampleSource,
                correlationId: "catalog-webview-png"
            ),
            nativePayload: mermaidNativePNGPayload(
                source: mermaidPlaygroundSampleSource,
                correlationId: "catalog-native-png"
            )
        ))

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func cellOwnershipMapConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Cell Ownership Map")
        configuration.description = "Obsidian-lignende graf over hvilke celler requesteren eier, har tilgang til, kjører lokalt, har persistent registrering eller kjenner som remote scaffold-ruter."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///EntityCellGraph",
            sourceCellName: "EntityCellGraphCell",
            purpose: "Cell ownership/access map",
            purposeDescription: "Synliggjør lokale eier-/tilgangsrelasjoner, runtime-celler, persistente celletyper og kjente remote routes uten å omgå resolver-policy.",
            interests: ["cellprotocol", "cells", "ownership", "access", "identity", "graph", "scaffold", "remote", "purposeRef=cell.access.graph.view"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var reference = CellReference(endpoint: "cell:///EntityCellGraph", subscribeFeed: false, label: "entityGraph")
        reference.setKeysAndValues = [
            KeyValue(key: CellAccessGraphContract.stateKeypath, value: nil),
            KeyValue(
                key: EntityCellGraphCell.visualizationKeypath,
                value: .object([
                    "cluster": .string("mine"),
                    "limit": .integer(240)
                ])
            )
        ]
        configuration.addReference(reference)

        var graphModifiers = SkeletonModifiers()
        graphModifiers.height = 620
        graphModifiers.maxWidthInfinity = true
        graphModifiers.styleRole = "entity-cell-graph"

        var elements = SkeletonElementList()
        elements.append(catalogText("Cell Ownership Map"))
        elements.append(catalogText("Dette kartet viser hva requesteren eier eller har tilgang til i denne scaffolden, samt aktive, persistente og kjente remote routes. Autoritet kommer fortsatt fra resolver/capability-grants, ikke fra at en node vises i grafen."))
        elements.append(
            catalogCardSection(
                "Runtime sync",
                content: [
                    dashboardKeyText("entityGraph.atlas.entityGraph.state.status", fontSize: 13, foregroundColor: "#8DE1DA"),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "entityGraph.\(EntityCellGraphCell.visualizationKeypath)",
                                label: "Sync local runtime",
                                payload: .object([
                                    "cluster": .string("mine"),
                                    "limit": .integer(240),
                                    "syncRuntime": .bool(true)
                                ])
                            ),
                            catalogButton(
                                keypath: "entityGraph.\(EntityCellGraphCell.visualizationKeypath)",
                                label: "Mine",
                                payload: .object(["cluster": .string("mine"), "limit": .integer(240)])
                            ),
                            catalogButton(
                                keypath: "entityGraph.\(EntityCellGraphCell.visualizationKeypath)",
                                label: "Active",
                                payload: .object(["cluster": .string("active"), "limit": .integer(240)])
                            ),
                            catalogButton(
                                keypath: "entityGraph.\(EntityCellGraphCell.visualizationKeypath)",
                                label: "Persistent",
                                payload: .object(["cluster": .string("persisted"), "limit": .integer(240)])
                            ),
                            catalogButton(
                                keypath: "entityGraph.\(EntityCellGraphCell.visualizationKeypath)",
                                label: "Remote routes",
                                payload: .object(["cluster": .string("remote"), "limit": .integer(240)])
                            ),
                            catalogButton(
                                keypath: "entityGraph.\(EntityCellGraphCell.visualizationKeypath)",
                                label: "All",
                                payload: .object(["cluster": .string("all"), "limit": .integer(320)])
                            )
                        ])
                    ),
                    .Grid(
                        SkeletonGrid(
                            columns: [.adaptive(min: 120, max: 180)],
                            spacing: 10,
                            elements: [
                                dashboardBadgeKeyText("entityGraph.atlas.entityGraph.state.nodes"),
                                dashboardBadgeKeyText("entityGraph.atlas.entityGraph.state.edges"),
                                dashboardBadgeKeyText("entityGraph.atlas.entityGraph.state.activeCells"),
                                dashboardBadgeKeyText("entityGraph.atlas.entityGraph.state.persistentCellTypes"),
                                dashboardBadgeKeyText("entityGraph.atlas.entityGraph.state.remoteScaffolds")
                            ]
                        )
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Graph",
                content: [
                    dashboardKeyText("entityGraph.atlas.entityGraph.visualization.summaryText", fontSize: 13, foregroundColor: "#9AC4CF"),
                    .Visualization(
                        SkeletonVisualization(
                            kind: "network",
                            keypath: "entityGraph.\(EntityCellGraphCell.visualizationKeypath)",
                            stateKeypath: "entityGraph.\(EntityCellGraphCell.visualizationKeypath)",
                            actionKeypath: "entityGraph.\(EntityCellGraphCell.visualizationKeypath)",
                            modifiers: graphModifiers
                        )
                    ),
                    dashboardKeyText("entityGraph.atlas.entityGraph.visualization.remoteInventoryHint", fontSize: 12, foregroundColor: "#9AC4CF")
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Selected node",
                content: [
                    dashboardKeyText("entityGraph.atlas.entityGraph.visualization.selectedNode.label", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                    dashboardKeyText("entityGraph.atlas.entityGraph.visualization.selectedNode.kind", fontSize: 12, foregroundColor: "#8DE1DA"),
                    dashboardKeyText("entityGraph.atlas.entityGraph.visualization.selectedNode.runtimeState", fontSize: 12, foregroundColor: "#F6C66F"),
                    dashboardKeyText("entityGraph.atlas.entityGraph.visualization.selectedNode.domain", fontSize: 12, foregroundColor: "#D5E4ED"),
                    dashboardKeyText("entityGraph.atlas.entityGraph.visualization.selectedNode.id", fontSize: 12, foregroundColor: "#9AC4CF")
                ]
            )
        )

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func conferenceOwnershipDiagramConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Conference Ownership Diagram")
        configuration.description = "Render den kanoniske konferanse-dokumentasjonen for dataflyt og eierskap via MarkdownRenderer og MermaidRenderer."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///MarkdownRenderer",
            sourceCellName: "MarkdownRendererCell",
            purpose: "Konferanse ownership- og dataflytdiagram",
            purposeDescription: "Viser det kanoniske bokdokumentet for conference ownership/dataflow og renderer Mermaid-diagrammet inline.",
            interests: ["conference", "ownership", "dataflow", "documentation", "mermaid", "access"],
            menuSlots: ["upperLeft", "lowerLeft"]
        )

        var reference = CellReference(endpoint: "cell:///MarkdownRenderer", label: "markdownRenderer")
        reference.setKeysAndValues = [
            KeyValue(key: "state", value: nil),
            KeyValue(key: "render.markdown", value: .object(conferenceOwnershipDiagramRenderPayload(backend: .web)))
        ]
        configuration.addReference(reference)

        var elements = SkeletonElementList()
        elements.append(catalogText("Conference Ownership Diagram"))
        elements.append(catalogText("Denne flaten bruker den kanoniske bok-siden for conference ownership/dataflow. Mermaid-blokken rendres av MarkdownRenderer, som igjen delegerer diagrammet til MermaidRenderer."))
        elements.append(contentsOf: conferenceOwnershipDiagramSections(referenceLabel: "markdownRenderer"))

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func conferenceSkeletonComponentLibraryConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Conference Skeleton Component Library")
        configuration.description = "Designsystem-flate for gjenbrukbare conference-seksjoner, state-kontrakter og actions som kan plukkes av både brukere og kodeassistenter."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConfigurationCatalog",
            sourceCellName: "ConfigurationCatalogCell",
            purpose: "Conference skeleton component library",
            purposeDescription: "Vis de gjenbrukbare conference-komponentene og hvilke keypaths/action-kontrakter de bygger på, slik at nye skeletoner kan lages uten å kopiere store config-blokker i blinde.",
            interests: ["conference", "skeleton", "components", "design-system", "library", "agent", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var reference = CellReference(endpoint: "cell:///ConfigurationCatalog", subscribeFeed: false, label: "configurationCatalog")
        reference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(reference)

        var elements = SkeletonElementList()
        elements.append(catalogText("Conference Skeleton Component Library"))
        elements.append(catalogText("Denne flaten samler de viktigste conference-byggesteinene i ett sted: hva komponenten gjør, hvilke state-keypaths den leser, hvilke actions den trenger og hvilke flater den passer i. Tanken er at både mennesker og kodeassistenter kan plukke herfra før de lager nye varianter."))
        elements.append(
            catalogCardSection(
                "Startpunkter",
                content: [
                    dashboardStaticText("Bruk disse flatene som kanoniske referanser når du vil se komponentene i full kontekst."),
                    launcherButtonRow([
                        loadConfigurationButton("Participant dashboard", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                        loadConfigurationButton("Public surface", configurationName: "Conference Public Surface", sourceCellEndpoint: "cell:///ConferencePublicShell")
                    ]),
                    launcherButtonRow([
                        loadConfigurationButton("Control tower", configurationName: "Conference Control Tower", sourceCellEndpoint: "cell:///ConferenceAdminPreviewShell"),
                        loadConfigurationButton("Sponsor follow-up", configurationName: "Conference Sponsor Follow-up", sourceCellEndpoint: "cell:///ConferenceSponsorPreviewShell")
                    ])
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Participant Variants",
                content: ConferenceShellConfigurationFactory.participantBuiltinVariants().map { variant in
                    dashboardStaticText("\(variant.displayName): \(variant.summary) [family=\(variant.styleProfile.family), tone=\(variant.styleProfile.tone ?? "default")]")
                }
            )
        )

        for component in ConferenceSkeletonComponentLibrary.components {
            let surfaces = component.surfaces.joined(separator: ", ")
            let stateKeys = component.stateKeypaths.joined(separator: " | ")
            let actionKeys = component.actionKeypaths.isEmpty ? "Read-only component" : component.actionKeypaths.joined(separator: " | ")
            elements.append(
                catalogCardSection(
                    component.displayName,
                    content: [
                        dashboardStaticText(component.summary),
                        dashboardStaticText("Brukes i: \(surfaces)"),
                        dashboardStaticText("State: \(stateKeys)"),
                        dashboardStaticText("Actions: \(actionKeys)"),
                        dashboardStaticText("Stilfamilie: \(component.styleFamily)"),
                        dashboardStaticText(component.notes)
                    ]
                )
            )
        }

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func conferenceParticipantPortalConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Conference Participant Portal Dashboard")
        configuration.description = "Ryddig participant dashboard som bruker en stabil preview-wrapper over ConferenceParticipantShell. Primærflaten viser hjem, agenda, folk, chat, møter og avanserte conference-verktøy i samme designspor."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
            sourceCellName: "ConferenceParticipantPreviewShellCell",
            purpose: "Conference participantportal",
            purposeDescription: "Primær deltakerflate for konferansen: vis neste steg, agenda, anbefalte personer, chat, møter og avanserte proof/session-verktøy med fungerende actions fra ConferenceParticipantShell.",
            interests: ["conference", "participant", "dashboard", "agenda", "people-discovery", "chat", "meetings", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var reference = CellReference(endpoint: "cell:///ConferenceParticipantPreviewShell", subscribeFeed: false, label: "conferenceParticipantShell")
        reference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(reference)

        var elements = SkeletonElementList()
        elements.append(conferenceParticipantPortalHeaderSection(referenceLabel: "conferenceParticipantShell"))
        elements.append(conferenceParticipantPortalPrimaryTabs(referenceLabel: "conferenceParticipantShell"))

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func conferencePublicSurfaceClaudeConfiguration() -> CellConfiguration {
        withClaudeVisualStyle(
            configuration: conferencePublicSurfaceConfiguration(),
            name: "Conference Public Surface Claude",
            uuidSeed: "conference-public-surface-claude",
            description: "Claude visual parity variant of the public conference surface. It preserves the same ConferencePublicShell reference contract as the existing public configuration.",
            purpose: "Conference public website Claude parity",
            purposeDescription: "Public-facing Claude design variant over the same ConferencePublicShell data model: warm paper, editorial hero, indigo calls to action, and the same public track/session/person refs.",
            extraInterests: ["claude-design", "visual-parity", "warm-paper", "public"],
            styleClass: "conference-claude-public"
        )
    }

    static func conferenceParticipantPortalClaudeConfiguration() -> CellConfiguration {
        withClaudeVisualStyle(
            configuration: conferenceParticipantPortalConfiguration(),
            name: "Conference Participant Portal Claude",
            uuidSeed: "conference-participant-portal-claude",
            description: "Claude visual parity variant of the participant portal. It preserves the same ConferenceParticipantPreviewShell cell reference as the existing dashboard.",
            purpose: "Conference participantportal Claude parity",
            purposeDescription: "Participant day-workspace variant over the same ConferenceParticipantPreviewShell data model: warm paper surface, lavender/indigo tabs, agenda cards, people, chat and meetings from the same keypaths.",
            extraInterests: ["claude-design", "visual-parity", "participant", "day-workspace"],
            styleClass: "conference-claude-participant"
        )
    }

    static func conferenceParticipantChatClaudeConfiguration() -> CellConfiguration {
        withClaudeVisualStyle(
            configuration: conferenceParticipantChatConfiguration(),
            name: "Conference Participant Chat Claude",
            uuidSeed: "conference-participant-chat-claude",
            description: "Claude visual parity variant of the participant chat surface. It preserves ConferenceChatLaunch and participant preview references.",
            purpose: "Conference participant chat Claude parity",
            purposeDescription: "Warm proof/chat variant over the same ConferenceChatLaunch and participant preview data: chat rows, member invites and tool cards retain their existing actions.",
            extraInterests: ["claude-design", "visual-parity", "participant", "chat", "proof"],
            styleClass: "conference-claude-chat"
        )
    }

    static func conferenceControlTowerClaudeConfiguration() -> CellConfiguration {
        withClaudeVisualStyle(
            configuration: conferenceControlTowerConfiguration(),
            name: "Conference Control Tower Claude",
            uuidSeed: "conference-control-tower-claude",
            description: "Claude visual parity variant of the organizer control tower. It preserves the same admin preview and broadcast studio references.",
            purpose: "Conference control tower Claude parity",
            purposeDescription: "Organizer variant over the same ConferenceAdminPreviewShell and ConferenceBroadcastStudio data model: warm paper surface, amber admin state, KPI cards and consent-safe aggregate views.",
            extraInterests: ["claude-design", "visual-parity", "organizer", "control-tower"],
            styleClass: "conference-claude-admin"
        )
    }

    static func conferenceSponsorClaudeConfiguration() -> CellConfiguration {
        withClaudeVisualStyle(
            configuration: ConferenceShellConfigurationFactory.makeSponsorConfiguration(),
            name: "Conference Sponsor Follow-up Claude",
            uuidSeed: "conference-sponsor-follow-up-claude",
            description: "Claude visual parity variant of the sponsor follow-up surface. It preserves the same ConferenceSponsorPreviewShell reference as the existing sponsor configuration.",
            purpose: "Conference sponsor follow-up Claude parity",
            purposeDescription: "Sponsor variant over the same ConferenceSponsorPreviewShell data model: green consent pipeline, lead inbox, agreement receipts and retention queues without changing sponsor ownership.",
            extraInterests: ["claude-design", "visual-parity", "sponsor", "consent"],
            styleClass: "conference-claude-sponsor"
        )
    }

    static func conferenceNearbyRadarClaudeConfiguration() -> CellConfiguration {
        withClaudeVisualStyle(
            configuration: conferenceNearbyRadarConfiguration(),
            name: "Conference Nearby Radar Claude",
            uuidSeed: "conference-nearby-radar-claude",
            description: "Claude visual parity variant of the nearby radar surface. It preserves the same participant preview discovery reference.",
            purpose: "Conference nearby radar Claude parity",
            purposeDescription: "Blue signal/radar variant over the same ConferenceParticipantPreviewShell discovery state. Binding can still project native scanner encounters into the same rows.",
            extraInterests: ["claude-design", "visual-parity", "nearby", "radar", "scanner"],
            styleClass: "conference-claude-nearby"
        )
    }

    private static func withClaudeVisualStyle(
        configuration: CellConfiguration,
        name: String,
        uuidSeed: String,
        description: String,
        purpose: String,
        purposeDescription: String,
        extraInterests: [String],
        styleClass: String
    ) -> CellConfiguration {
        var configuration = configuration
        let baseDiscovery = configuration.discovery
        configuration.name = name
        configuration.uuid = stableUUID(seed: uuidSeed).uuidString
        configuration.description = description
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: baseDiscovery?.sourceCellEndpoint,
            sourceCellName: baseDiscovery?.sourceCellName,
            purpose: purpose,
            purposeDescription: purposeDescription,
            interests: mergedInterests(baseDiscovery?.interests ?? [], extraInterests),
            purposeRefs: baseDiscovery?.purposeRefs ?? [],
            interestRefs: baseDiscovery?.interestRefs ?? [],
            menuSlots: baseDiscovery?.menuSlots ?? ["upperMid", "lowerMid"],
            localizedText: baseDiscovery?.localizedText ?? [:]
        )

        if let skeleton = configuration.skeleton {
            let remapped = remapConfigurationLookups(in: skeleton, nameMap: claudeConfigurationLookupMap)
            let retinted = retintClaudeVisuals(in: remapped, styleClass: styleClass)
            configuration.skeleton = applyingClaudeRootStyle(retinted, styleClass: styleClass)
        }
        return configuration
    }

    private static var claudeConfigurationLookupMap: [String: String] {
        [
            "Conference Public Surface": "Conference Public Surface Claude",
            conferenceParticipantPortalLoadConfigurationName: "Conference Participant Portal Claude",
            "Conference Participant Chat": "Conference Participant Chat Claude",
            "Conference Control Tower": "Conference Control Tower Claude",
            "Conference Sponsor Follow-up": "Conference Sponsor Follow-up Claude",
            "Conference Nearby Radar": "Conference Nearby Radar Claude"
        ]
    }

    private static func mergedInterests(_ base: [String], _ extra: [String]) -> [String] {
        var seen = Set<String>()
        var merged: [String] = []
        for value in base + extra {
            let trimmed = value.trimmingCharacters(in: .whitespacesAndNewlines)
            guard trimmed.isEmpty == false, seen.insert(trimmed).inserted else {
                continue
            }
            merged.append(trimmed)
        }
        return merged
    }

    private static func applyingClaudeRootStyle(_ element: SkeletonElement, styleClass: String) -> SkeletonElement {
        guard case var .VStack(stack) = element else {
            return element
        }
        stack.modifiers = appendingStyleClasses(
            stack.modifiers,
            ["conference-claude-shell", styleClass],
            styleRole: "conference-claude"
        )
        return .VStack(stack)
    }

    private enum ClaudeModifierRole {
        case root
        case section
        case text
        case button
        case input
        case image
        case list
        case container
        case other
    }

    // XCTest/Vapor async worker threads can have small stacks; deep factory
    // decoration should degrade instead of risking SIGBUS from stack overflow.
    private static let configurationSkeletonDecorationMaxDepth = 5
    private static let configurationSkeletonLookupRemapMaxDepth = 16

    private static func retintClaudeChild(
        _ element: SkeletonElement,
        styleClass: String,
        depth: Int
    ) -> SkeletonElement {
        let childDepth = depth + 1
        guard childDepth < configurationSkeletonDecorationMaxDepth else {
            return element
        }
        return retintClaudeVisuals(in: element, styleClass: styleClass, depth: childDepth)
    }

    private static func retintClaudeChildStack(
        _ stack: SkeletonVStack,
        styleClass: String,
        depth: Int
    ) -> SkeletonVStack {
        let childDepth = depth + 1
        guard childDepth < configurationSkeletonDecorationMaxDepth else {
            return stack
        }
        return retintClaudeVisuals(in: stack, styleClass: styleClass, depth: childDepth)
    }

    private static func retintClaudeVisuals(
        in stack: SkeletonVStack,
        styleClass: String,
        depth: Int = 0
    ) -> SkeletonVStack {
        guard depth < configurationSkeletonDecorationMaxDepth else {
            return stack
        }

        var stack = stack
        stack.modifiers = retintClaudeModifiers(stack.modifiers, styleClass: styleClass, role: .container)
        stack.elements = stack.elements.map { retintClaudeChild($0, styleClass: styleClass, depth: depth) }
        return stack
    }

    private static func retintClaudeVisuals(
        in element: SkeletonElement,
        styleClass: String,
        depth: Int = 0
    ) -> SkeletonElement {
        guard depth < configurationSkeletonDecorationMaxDepth else {
            return element
        }

        switch element {
        case .Text(var text):
            text.modifiers = retintClaudeModifiers(text.modifiers, styleClass: styleClass, role: .text)
            return .Text(text)
        case .Button(var button):
            button.modifiers = retintClaudeModifiers(button.modifiers, styleClass: styleClass, role: .button)
            return .Button(button)
        case .TextField(var textField):
            textField.modifiers = retintClaudeModifiers(textField.modifiers, styleClass: styleClass, role: .input)
            return .TextField(textField)
        case .TextArea(var textArea):
            textArea.modifiers = retintClaudeModifiers(textArea.modifiers, styleClass: styleClass, role: .input)
            return .TextArea(textArea)
        case .AttachmentField(var attachment):
            attachment.modifiers = retintClaudeModifiers(attachment.modifiers, styleClass: styleClass, role: .input)
            return .AttachmentField(attachment)
        case .FileUpload(var upload):
            upload.modifiers = retintClaudeModifiers(upload.modifiers, styleClass: styleClass, role: .input)
            return .FileUpload(upload)
        case .Image(var image):
            image.modifiers = retintClaudeModifiers(image.modifiers, styleClass: styleClass, role: .image)
            return .Image(image)
        case .Spacer(var spacer):
            spacer.modifiers = retintClaudeModifiers(spacer.modifiers, styleClass: styleClass, role: .other)
            return .Spacer(spacer)
        case .HStack(var stack):
            stack.modifiers = retintClaudeModifiers(stack.modifiers, styleClass: styleClass, role: .container)
            stack.elements = stack.elements.map { retintClaudeChild($0, styleClass: styleClass, depth: depth) }
            return .HStack(stack)
        case .VStack(var stack):
            stack = retintClaudeVisuals(in: stack, styleClass: styleClass, depth: depth)
            return .VStack(stack)
        case .ZStack(var stack):
            stack.modifiers = retintClaudeModifiers(stack.modifiers, styleClass: styleClass, role: .container)
            stack.elements = stack.elements.map { retintClaudeChild($0, styleClass: styleClass, depth: depth) }
            return .ZStack(stack)
        case .ScrollView(var scrollView):
            scrollView.modifiers = retintClaudeModifiers(scrollView.modifiers, styleClass: styleClass, role: .container)
            scrollView.elements = scrollView.elements.map { retintClaudeChild($0, styleClass: styleClass, depth: depth) }
            return .ScrollView(scrollView)
        case .Section(var section):
            section.modifiers = retintClaudeModifiers(section.modifiers, styleClass: styleClass, role: .section)
            if let header = section.header {
                section.header = retintClaudeChild(header, styleClass: styleClass, depth: depth)
            }
            if let footer = section.footer {
                section.footer = retintClaudeChild(footer, styleClass: styleClass, depth: depth)
            }
            section.content = section.content.map { retintClaudeChild($0, styleClass: styleClass, depth: depth) }
            return .Section(section)
        case .Tabs(var tabs):
            tabs.modifiers = retintClaudeModifiers(tabs.modifiers, styleClass: styleClass, role: .container)
            tabs.panels = tabs.panels.map { panel in
                var panel = panel
                panel.modifiers = retintClaudeModifiers(panel.modifiers, styleClass: styleClass, role: .container)
                panel.content = panel.content.map { retintClaudeChild($0, styleClass: styleClass, depth: depth) }
                return panel
            }
            return .Tabs(tabs)
        case .List(var list):
            list.modifiers = retintClaudeModifiers(list.modifiers, styleClass: styleClass, role: .list)
            if let row = list.flowElementSkeleton {
                list.flowElementSkeleton = retintClaudeChildStack(row, styleClass: styleClass, depth: depth)
            }
            return .List(list)
        case .Reference(var reference):
            reference.modifiers = retintClaudeModifiers(reference.modifiers, styleClass: styleClass, role: .list)
            if let row = reference.flowElementSkeleton {
                reference.flowElementSkeleton = retintClaudeChildStack(row, styleClass: styleClass, depth: depth)
            }
            return .Reference(reference)
        case .Grid(var grid):
            grid.modifiers = retintClaudeModifiers(grid.modifiers, styleClass: styleClass, role: .list)
            if let item = grid.itemSkeleton {
                grid.itemSkeleton = retintClaudeChild(item, styleClass: styleClass, depth: depth)
            }
            grid.elements = grid.elements.map { retintClaudeChild($0, styleClass: styleClass, depth: depth) }
            return .Grid(grid)
        case .Object(var object):
            object.modifiers = retintClaudeModifiers(object.modifiers, styleClass: styleClass, role: .container)
            object.elements = object.elements.mapValues { retintClaudeChild($0, styleClass: styleClass, depth: depth) }
            return .Object(object)
        case .Toggle(var toggle):
            toggle.modifiers = retintClaudeModifiers(toggle.modifiers, styleClass: styleClass, role: .input)
            return .Toggle(toggle)
        case .Picker(var picker):
            picker.modifiers = retintClaudeModifiers(picker.modifiers, styleClass: styleClass, role: .input)
            return .Picker(picker)
        case .Visualization(var visualization):
            visualization.modifiers = retintClaudeModifiers(visualization.modifiers, styleClass: styleClass, role: .section)
            return .Visualization(visualization)
        case .Divider:
            return element
        default:
            return element
        }
    }

    private static func retintClaudeModifiers(
        _ modifiers: SkeletonModifiers?,
        styleClass: String,
        role: ClaudeModifierRole
    ) -> SkeletonModifiers? {
        var modifiers = modifiers ?? SkeletonModifiers()
        let accent = claudeAccentColor(for: styleClass)

        switch role {
        case .root:
            modifiers.background = "#F7F5EF"
            modifiers.foregroundColor = "#171717"
        case .section:
            modifiers.background = "#FFFFFF"
            modifiers.borderColor = "#D9D5CB"
            modifiers.borderWidth = max(modifiers.borderWidth ?? 0, 1)
            modifiers.cornerRadius = min(modifiers.cornerRadius ?? 10, 10)
            modifiers.padding = max(modifiers.padding ?? 0, 14)
            modifiers.foregroundColor = "#171717"
            modifiers.shadowRadius = max(modifiers.shadowRadius ?? 0, 14)
            modifiers.shadowX = modifiers.shadowX ?? 0
            modifiers.shadowY = modifiers.shadowY ?? 8
            modifiers.shadowColor = "#433A2914"
        case .text:
            modifiers.foregroundColor = "#171717"
        case .button:
            modifiers.background = accent
            modifiers.borderColor = accent
            modifiers.borderWidth = max(modifiers.borderWidth ?? 0, 1)
            modifiers.cornerRadius = min(modifiers.cornerRadius ?? 8, 8)
            modifiers.foregroundColor = "#FFFFFF"
        case .input:
            modifiers.background = "#FFFFFF"
            modifiers.borderColor = "#D9D5CB"
            modifiers.borderWidth = max(modifiers.borderWidth ?? 0, 1)
            modifiers.cornerRadius = min(modifiers.cornerRadius ?? 8, 8)
            modifiers.foregroundColor = "#171717"
        case .image:
            modifiers.background = "#FBFAF6"
            modifiers.borderColor = "#D9D5CB"
            modifiers.borderWidth = max(modifiers.borderWidth ?? 0, 1)
            modifiers.cornerRadius = min(modifiers.cornerRadius ?? 10, 10)
        case .list:
            if modifiers.background != nil {
                modifiers.background = "#FBFAF6"
            }
            if modifiers.borderColor != nil {
                modifiers.borderColor = "#D9D5CB"
            }
            modifiers.foregroundColor = "#171717"
        case .container:
            if modifiers.background != nil {
                modifiers.background = "#F7F5EF"
            }
            modifiers.foregroundColor = "#171717"
        case .other:
            break
        }

        return modifiers
    }

    private static func claudeAccentColor(for styleClass: String) -> String {
        if styleClass.contains("admin") {
            return "#B76A00"
        }
        if styleClass.contains("sponsor") {
            return "#0B7A5A"
        }
        if styleClass.contains("nearby") {
            return "#2F65B8"
        }
        return "#5B4BC8"
    }

    private static func appendingStyleClasses(
        _ modifiers: SkeletonModifiers?,
        _ styleClasses: [String],
        styleRole: String? = nil
    ) -> SkeletonModifiers {
        var modifiers = modifiers ?? SkeletonModifiers()
        var existing = modifiers.styleClasses ?? []
        for styleClass in styleClasses where existing.contains(styleClass) == false {
            existing.append(styleClass)
        }
        modifiers.styleClasses = existing
        if let styleRole {
            modifiers.styleRole = styleRole
        }
        return modifiers
    }

    private static func remapConfigurationLookups(
        in stack: SkeletonVStack,
        nameMap: [String: String],
        depth: Int = 0
    ) -> SkeletonVStack {
        guard depth < configurationSkeletonLookupRemapMaxDepth else {
            return stack
        }

        var stack = stack
        stack.elements = stack.elements.map { remapConfigurationLookupChild($0, nameMap: nameMap, depth: depth) }
        return stack
    }

    private static func remapConfigurationLookupChild(
        _ element: SkeletonElement,
        nameMap: [String: String],
        depth: Int
    ) -> SkeletonElement {
        let childDepth = depth + 1
        guard childDepth < configurationSkeletonLookupRemapMaxDepth else {
            return element
        }
        return remapConfigurationLookups(in: element, nameMap: nameMap, depth: childDepth)
    }

    private static func remapConfigurationLookupChildStack(
        _ stack: SkeletonVStack,
        nameMap: [String: String],
        depth: Int
    ) -> SkeletonVStack {
        let childDepth = depth + 1
        guard childDepth < configurationSkeletonLookupRemapMaxDepth else {
            return stack
        }
        return remapConfigurationLookups(in: stack, nameMap: nameMap, depth: childDepth)
    }

    private static func remapConfigurationLookups(
        in element: SkeletonElement,
        nameMap: [String: String],
        depth: Int = 0
    ) -> SkeletonElement {
        guard depth < configurationSkeletonLookupRemapMaxDepth else {
            return element
        }

        switch element {
        case .Button(var button):
            button.payload = remapConfigurationLookupPayload(button.payload, nameMap: nameMap)
            return .Button(button)
        case .HStack(var stack):
            stack.elements = stack.elements.map { remapConfigurationLookupChild($0, nameMap: nameMap, depth: depth) }
            return .HStack(stack)
        case .VStack(var stack):
            stack = remapConfigurationLookups(in: stack, nameMap: nameMap, depth: depth)
            return .VStack(stack)
        case .ZStack(var stack):
            stack.elements = stack.elements.map { remapConfigurationLookupChild($0, nameMap: nameMap, depth: depth) }
            return .ZStack(stack)
        case .ScrollView(var scrollView):
            scrollView.elements = scrollView.elements.map { remapConfigurationLookupChild($0, nameMap: nameMap, depth: depth) }
            return .ScrollView(scrollView)
        case .Section(var section):
            if let header = section.header {
                section.header = remapConfigurationLookupChild(header, nameMap: nameMap, depth: depth)
            }
            if let footer = section.footer {
                section.footer = remapConfigurationLookupChild(footer, nameMap: nameMap, depth: depth)
            }
            section.content = section.content.map { remapConfigurationLookupChild($0, nameMap: nameMap, depth: depth) }
            return .Section(section)
        case .Tabs(var tabs):
            tabs.panels = tabs.panels.map { panel in
                var panel = panel
                panel.content = panel.content.map { remapConfigurationLookupChild($0, nameMap: nameMap, depth: depth) }
                return panel
            }
            return .Tabs(tabs)
        case .List(var list):
            if let row = list.flowElementSkeleton {
                list.flowElementSkeleton = remapConfigurationLookupChildStack(row, nameMap: nameMap, depth: depth)
            }
            return .List(list)
        case .Reference(var reference):
            if let row = reference.flowElementSkeleton {
                reference.flowElementSkeleton = remapConfigurationLookupChildStack(row, nameMap: nameMap, depth: depth)
            }
            return .Reference(reference)
        case .Grid(var grid):
            if let item = grid.itemSkeleton {
                grid.itemSkeleton = remapConfigurationLookupChild(item, nameMap: nameMap, depth: depth)
            }
            grid.elements = grid.elements.map { remapConfigurationLookupChild($0, nameMap: nameMap, depth: depth) }
            return .Grid(grid)
        case .Object(var object):
            object.elements = object.elements.mapValues { remapConfigurationLookupChild($0, nameMap: nameMap, depth: depth) }
            return .Object(object)
        default:
            return element
        }
    }

    private static func remapConfigurationLookupPayload(
        _ payload: ValueType?,
        nameMap: [String: String]
    ) -> ValueType? {
        guard case var .object(payloadObject)? = payload,
              case var .object(lookup)? = payloadObject["configurationLookup"],
              case let .string(currentName)? = lookup["name"],
              let replacement = nameMap[currentName] else {
            return payload
        }

        lookup["name"] = .string(replacement)
        payloadObject["configurationLookup"] = .object(lookup)
        return .object(payloadObject)
    }

    private static func conferenceParticipantPortalPrimaryTabs(referenceLabel: String) -> SkeletonElement {
        .Tabs(
            SkeletonTabs(
                id: stableUUID(seed: "conference-participant-portal-primary-tabs"),
                tabsKeypath: "\(referenceLabel).state.navigation.tabs",
                activeTabStateKeypath: "\(referenceLabel).state.navigation.activeTab",
                selectionActionKeypath: "\(referenceLabel).navigation.setActiveTab",
                panels: [
                    SkeletonTabPanel(
                        id: "today",
                        content: [
                            conferenceParticipantPortalHomeSection(referenceLabel: referenceLabel)
                        ]
                    ),
                    SkeletonTabPanel(
                        id: "agenda",
                        content: [
                            conferenceParticipantPortalAgendaCleanSection(referenceLabel: referenceLabel)
                        ]
                    ),
                    SkeletonTabPanel(
                        id: "people",
                        content: [
                            conferenceParticipantPortalPeopleSection(referenceLabel: referenceLabel)
                        ]
                    ),
                    SkeletonTabPanel(
                        id: "chats",
                        content: [
                            conferenceParticipantPortalDirectChatCleanSection(referenceLabel: referenceLabel),
                            conferenceParticipantPortalAppendixSection(referenceLabel: referenceLabel)
                        ]
                    ),
                    SkeletonTabPanel(
                        id: "meetings",
                        content: [
                            conferenceParticipantPortalMeetingsSection(referenceLabel: referenceLabel)
                        ]
                    ),
                    SkeletonTabPanel(
                        id: "profile",
                        content: [
                            conferenceParticipantPortalProfilePrivacySection(referenceLabel: referenceLabel)
                        ]
                    )
                ]
            )
        )
    }

    private static func conferenceParticipantPortalHeaderSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Conference Participant Portal Dashboard",
            content: [
                dashboardKeyText("\(referenceLabel).state.workspace.title", fontSize: 20, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("\(referenceLabel).state.workspace.participantBadge"),
                dashboardKeyText("\(referenceLabel).state.workspace.conferenceBadge"),
                dashboardKeyText("\(referenceLabel).state.workspace.nextStep"),
                .HStack(SkeletonHStack(elements: [
                    loadConfigurationButton("Åpne AI-assistent", configurationName: "Conference AI Assistant", sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell"),
                    loadConfigurationButton("Åpne chatflate", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch")
                ]))
            ]
        )
    }

    private static func conferenceParticipantPortalHomeSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Hjem",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 220, max: 300)],
                        spacing: 12,
                        keypath: "\(referenceLabel).state.workspace.pulseCards",
                        itemSkeleton: conferenceParticipantPortalCardSkeleton()
                    )
                ),
                dashboardStaticText("Neste sesjon", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.title", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.subtitle"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.detail"),
                .HStack(SkeletonHStack(elements: [
                    participantPortalActionButton(
                        referenceLabel,
                        actionKeypath: "agenda.toggleSelectedSessionSaved",
                        label: "Lagre/fjern valgt",
                        payload: .object([:])
                    ),
                    loadConfigurationButton(
                        "Åpne sesjonsdetaljer",
                        configurationName: "Conference Agenda Session Detail",
                        sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell"
                    )
                ]))
            ]
        )
    }

    private static func conferenceParticipantPortalAgendaCleanSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Min Agenda",
            content: [
                dashboardKeyText("\(referenceLabel).state.program.agendaSummary"),
                dashboardKeyText("\(referenceLabel).state.program.viewSummary"),
                dashboardStaticText("Spor", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                multiSelectableDashboardList(
                    keypath: "\(referenceLabel).state.program.trackOptions",
                    selectionStateKeypath: "\(referenceLabel).state.program.focusedTrackIDs",
                    selectionActionKeypath: "\(referenceLabel).agenda.setFocusedTracks",
                    rowSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: true),
                    styleClasses: ["conference-agenda-track-grid", "conference-agenda-card-list"],
                    allowsEmptySelection: true
                ),
                .Tabs(
                    SkeletonTabs(
                        id: stableUUID(seed: "conference-participant-portal-agenda-tabs:\(referenceLabel)"),
                        tabsKeypath: "\(referenceLabel).state.program.agendaTabs",
                        activeTabStateKeypath: "\(referenceLabel).state.program.activeView",
                        selectionActionKeypath: "\(referenceLabel).agenda.setView",
                        panels: [
                            SkeletonTabPanel(
                                id: "saved",
                                content: conferenceParticipantPortalAgendaTabContent(
                                    referenceLabel: referenceLabel,
                                    heading: "Valgte sesjoner",
                                    summaryKeypath: "\(referenceLabel).state.program.savedSummary",
                                    listKeypath: "\(referenceLabel).state.program.savedSessions"
                                )
                            ),
                            SkeletonTabPanel(
                                id: "forYou",
                                content: conferenceParticipantPortalAgendaTabContent(
                                    referenceLabel: referenceLabel,
                                    heading: "Anbefalte sesjoner",
                                    summaryKeypath: "\(referenceLabel).state.program.recommendedSummary",
                                    listKeypath: "\(referenceLabel).state.program.recommendedSessions"
                                )
                            ),
                            SkeletonTabPanel(
                                id: "focusedTracks",
                                content: conferenceParticipantPortalAgendaTabContent(
                                    referenceLabel: referenceLabel,
                                    heading: "Fra valgte spor",
                                    summaryKeypath: "\(referenceLabel).state.program.trackSummary",
                                    listKeypath: "\(referenceLabel).state.program.timelineSessions"
                                )
                            ),
                            SkeletonTabPanel(
                                id: "timeline",
                                content: conferenceParticipantPortalAgendaTabContent(
                                    referenceLabel: referenceLabel,
                                    heading: "Alle sesjoner",
                                    summaryKeypath: "\(referenceLabel).state.program.timelineSummary",
                                    listKeypath: "\(referenceLabel).state.program.timelineSessions"
                                )
                            )
                        ]
                    )
                ),
                dashboardStaticText("Valgt sesjon", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.title"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.subtitle"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.detail"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.note"),
                .HStack(SkeletonHStack(elements: [
                    participantPortalActionButton(referenceLabel, actionKeypath: "agenda.toggleSelectedSessionSaved", label: "Lagre/fjern valgt", payload: .object([:])),
                    loadConfigurationButton("Åpne sesjonsdetaljer", configurationName: "Conference Agenda Session Detail", sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell"),
                    loadConfigurationButton("Åpne spor-detaljer", configurationName: "Conference Agenda Track Detail", sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell")
                ]))
            ]
        )
    }

    private static func conferenceParticipantPortalAgendaTabContent(
        referenceLabel: String,
        heading: String,
        summaryKeypath: String,
        listKeypath: String
    ) -> SkeletonElementList {
        [
            dashboardStaticText(heading, fontWeight: "semibold", foregroundColor: "#F5FBFF"),
            dashboardKeyText(summaryKeypath),
            selectableDashboardList(
                keypath: listKeypath,
                selectionStateKeypath: "\(referenceLabel).state.program.selectedSessionID",
                selectionActionKeypath: "\(referenceLabel).agenda.selectSession",
                rowSkeleton: conferenceParticipantPortalSessionRowSkeleton(),
                styleClasses: ["conference-agenda-session-list", "conference-agenda-card-list"]
            )
        ]
    }

    private static func conferenceParticipantPortalPeopleSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Folk",
            content: [
                dashboardStaticText("Anbefalte kontakter", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("\(referenceLabel).state.matches.recommendationSummary"),
                .TextField(
                    SkeletonTextField(
                        text: nil,
                        sourceKeypath: "\(referenceLabel).state.matches.editor.query",
                        targetKeypath: "\(referenceLabel).matchmaking.searchPeople",
                        placeholder: "Søk etter folk, selskap eller tema"
                    )
                ),
                participantPortalDirectActionButton(
                    keypath: "\(referenceLabel).matchmaking.searchPeople",
                    label: "Søk"
                ),
                selectableDashboardList(
                    keypath: "\(referenceLabel).state.matches.recommendations",
                    selectionStateKeypath: "\(referenceLabel).state.discovery.selectedCandidateID",
                    selectionActionKeypath: "\(referenceLabel).discovery.selectCandidate",
                    rowSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: true, includeAction: true, includeMeetingAction: true)
                ),
                participantPortalActionButton(referenceLabel, actionKeypath: "matchmaking.refreshRecommendations", label: "Oppdater anbefalinger", payload: .object([:])),
                dashboardStaticText("Søkeresultat fra søkefeltet", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("\(referenceLabel).state.matches.searchSummary"),
                selectableDashboardList(
                    keypath: "\(referenceLabel).state.matches.searchResults",
                    selectionStateKeypath: "\(referenceLabel).state.discovery.selectedCandidateID",
                    selectionActionKeypath: "\(referenceLabel).discovery.selectCandidate",
                    rowSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: true, includeAction: true, includeMeetingAction: true)
                ),
                dashboardStaticText("Valgt kontakt", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("\(referenceLabel).state.discovery.selectionSummary")
            ]
        )
    }

    private static func conferenceParticipantPortalDirectChatCleanSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Direkte Chat",
            content: [
                dashboardKeyText("\(referenceLabel).state.chat.conversationSummary"),
                dashboardKeyText("\(referenceLabel).state.chat.nextAction"),
                .TextArea(
                    SkeletonTextArea(
                        text: nil,
                        sourceKeypath: "\(referenceLabel).state.chat.editor.draft",
                        targetKeypath: "\(referenceLabel).discoveryChat.setDraft",
                        placeholder: "Skriv en kort oppfølging",
                        minLines: 3,
                        maxLines: 6,
                        submitOnEnter: false,
                        editorMode: .plain
                    )
                ),
                .HStack(SkeletonHStack(elements: [
                    participantPortalActionButton(referenceLabel, actionKeypath: "discoveryChat.sendMessage", label: "Send melding", payload: .object([:])),
                    participantPortalActionButton(
                        referenceLabel,
                        actionKeypath: "discoveryChat.requestMemberInvite",
                        label: "Foreslå Samir",
                        payload: .object([
                            "targets": .list([
                                .object([
                                    "participantId": .string("participant-188"),
                                    "displayName": .string("Samir Iqbal"),
                                    "company": .string("Open Civic Labs"),
                                    "role": .string("organizer")
                                ])
                            ])
                        ])
                    ),
                    loadConfigurationButton("Åpne chatflate", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch")
                ])),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.chat.pendingMemberRequests",
                        flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: false)
                    )
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.chat.recentMessages",
                        flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: true)
                    )
                ),
                dashboardStaticText("Verktøy fra chat", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("\(referenceLabel).state.concierge.toolBoundary"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.concierge.toolCards",
                        flowElementSkeleton: conferenceParticipantPortalToolCardRowSkeleton()
                    )
                ),
                .HStack(SkeletonHStack(elements: [
                    participantPortalActionButton(
                        referenceLabel,
                        actionKeypath: "concierge.applyToolCard",
                        label: "Lag notatutkast",
                        payload: .object(["toolId": .string("draft-note")])
                    ),
                    participantPortalActionButton(
                        referenceLabel,
                        actionKeypath: "concierge.applyToolCard",
                        label: "Start prosjektutkast",
                        payload: .object(["toolId": .string("start-project")])
                    ),
                    participantPortalActionButton(
                        referenceLabel,
                        actionKeypath: "concierge.applyToolCard",
                        label: "Finn delt lokasjon",
                        payload: .object(["toolId": .string("find-peer-location")])
                    ),
                    participantPortalActionButton(
                        referenceLabel,
                        actionKeypath: "concierge.dismissToolCard",
                        label: "Skjul nearby-forslag",
                        payload: .object(["toolId": .string("nearby-invite")])
                    )
                ])),
                dashboardKeyText("\(referenceLabel).state.concierge.lastActionSummary")
            ]
        )
    }

    private static func conferenceParticipantPortalToolCardRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("statusLabel", fontSize: 12, foregroundColor: "#F6C66F"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED")
        ])
    }

    private static func conferenceParticipantPortalMeetingsSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Mine møter",
            content: [
                dashboardKeyText("\(referenceLabel).state.meetings.requestSummary"),
                dashboardKeyText("\(referenceLabel).state.meetings.meetingSummary"),
                dashboardKeyText("\(referenceLabel).state.meetings.exportStatus"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.meetings.requests",
                        flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: true, includeAction: true)
                    )
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.meetings.confirmedMeetings",
                        flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: false, includeAction: true)
                    )
                ),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "scheduling.exportICal",
                            label: "Forbered iCal",
                            payload: .bool(true)
                        )
                    ])
                )
            ]
        )
    }

    private static func conferenceParticipantPortalProfilePrivacySection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Profil og personvern",
            content: [
                dashboardKeyText("\(referenceLabel).state.onboarding.profileSummary"),
                dashboardKeyText("\(referenceLabel).state.onboarding.conferenceSummary"),
                dashboardKeyText("\(referenceLabel).state.onboarding.saveStatus"),
                dashboardKeyText("\(referenceLabel).state.onboarding.storageSummary"),
                dashboardStaticText("Formål", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                .List(SkeletonList(
                    topic: nil,
                    keypath: "\(referenceLabel).state.onboarding.purposes",
                    flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: false)
                )),
                dashboardStaticText("Interesser", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                .List(SkeletonList(
                    topic: nil,
                    keypath: "\(referenceLabel).state.onboarding.interests",
                    flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: false)
                )),
                dashboardStaticText("Samtykker", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                .List(SkeletonList(
                    topic: nil,
                    keypath: "\(referenceLabel).state.onboarding.consents",
                    flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: false)
                )),
                .HStack(SkeletonHStack(elements: [
                    loadConfigurationButton("Rediger onboarding", configurationName: "Conference Registration Setup", sourceCellEndpoint: "cell:///ConferenceOnboarding"),
                    loadConfigurationButton("Rediger offentlig profil", configurationName: "Conference Public Profile Editor", sourceCellEndpoint: "cell:///ConferencePublicProfileEditorPreview"),
                    loadConfigurationButton("Se offentlig profil", configurationName: "Conference Public Profile", sourceCellEndpoint: "cell:///ConferencePublicProfilePreview")
                ]))
            ]
        )
    }

    private static func conferenceParticipantPortalAppendixSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Avanserte verktøy",
            content: [
                dashboardStaticText("Avanserte konferanseverktøy som fortsatt følger samme skeleton-kontrakt. Bruk disse når du trenger proof-chat, session-tråd eller polling."),
                dashboardKeyText("\(referenceLabel).state.proofChat.status"),
                .HStack(SkeletonHStack(elements: [
                    participantPortalActionButton(referenceLabel, actionKeypath: "discovery.startProofChatWithSelectedCandidate", label: "Start proof-chat med valgt person", payload: .object([:])),
                    participantPortalActionButton(referenceLabel, actionKeypath: "proofChat.generateArtifacts", label: "Lag proof-artefakter", payload: .object([:]))
                ])),
                selectableDashboardList(
                    keypath: "\(referenceLabel).state.discovery.proofCandidates",
                    selectionStateKeypath: "\(referenceLabel).state.discovery.selectedProofCandidateID",
                    selectionActionKeypath: "\(referenceLabel).discovery.selectProofCandidate",
                    rowSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: true)
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.proofChat.messages",
                        flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: false)
                    )
                ),
                dashboardKeyText("\(referenceLabel).state.sessionThread.sessionSummary"),
                dashboardKeyText("\(referenceLabel).state.sessionPolling.questionSummary"),
                .HStack(SkeletonHStack(elements: [
                    participantPortalActionButton(
                        referenceLabel,
                        actionKeypath: "sessionThread.postMessage",
                        label: "Post spørsmål",
                        payload: .object(["text": .string("Hvordan bør vi ta dette videre etter sesjonen?")])
                    ),
                    participantPortalActionButton(
                        referenceLabel,
                        actionKeypath: "sessionPolling.vote",
                        label: "Stem nyttig nå",
                        payload: .object(["optionId": .string("immediately-useful")])
                    )
                ]))
            ]
        )
    }

    private static func conferenceParticipantPortalCardSkeleton() -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.background = "#122734"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#244457"

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED")
        ])
        section.modifiers = modifiers
        return .Section(section)
    }

    private static func conferenceParticipantPortalRowSkeleton(
        includeNote: Bool,
        includeAction: Bool = false,
        includeMeetingAction: Bool = false
    ) -> SkeletonVStack {
        var elements: SkeletonElementList = [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED")
        ]
        if includeNote {
            elements.append(dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"))
        }
        if includeAction {
            if includeMeetingAction {
                elements.append(.HStack(SkeletonHStack(elements: [
                    participantPortalRowActionButton(),
                    participantPortalRowMeetingButton()
                ])))
            } else {
                elements.append(participantPortalRowActionButton())
            }
        }
        return SkeletonVStack(elements: elements)
    }

    private static func conferenceParticipantPortalSessionRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            .HStack(SkeletonHStack(elements: [
                participantPortalRowActionButton(),
                participantPortalDetailRowButton()
            ]))
        ])
    }

    private static func conferenceParticipantPortalTimeSlotRowSkeleton(referenceLabel: String) -> SkeletonVStack {
        var rowModifiers = SkeletonModifiers()
        rowModifiers.padding = 14
        rowModifiers.background = "#101C25"
        rowModifiers.cornerRadius = 14
        rowModifiers.borderWidth = 1
        rowModifiers.borderColor = "#2A4A5F"
        rowModifiers.styleClasses = ["conference-agenda-timeslot-row"]

        var trackGridModifiers = SkeletonModifiers()
        trackGridModifiers.styleClasses = ["conference-agenda-timeslot-grid", "conference-agenda-timeslot-track-grid"]

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#A9C4D4"),
            .Grid(
                SkeletonGrid(
                    columns: [.adaptive(min: 220, max: 320)],
                    spacing: 12,
                    keypath: "trackCells",
                    itemSkeleton: dashboardAgendaTimeSlotTrackCellSkeleton(referenceLabel: referenceLabel),
                    modifiers: trackGridModifiers
                )
            )
        ])
        section.modifiers = rowModifiers
        return SkeletonVStack(elements: [.Section(section)])
    }

    static func conferenceDemoLauncherConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Conference Demo Launcher")
        configuration.description = "Deterministisk launcher for konferansedemoen. Åpner eksisterende conference-konfigurasjoner i fast rekkefølge uten biblioteksøk eller skjulte snarveier."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConfigurationCatalog",
            sourceCellName: "ConfigurationCatalogCell",
            purpose: "Conference demo launcher",
            purposeDescription: "Fast startflate for den library-first konferansedemoen. Hver knapp laster en eksisterende CellConfiguration i samme Porthole-session.",
            interests: ["conference", "demo", "launcher", "participant", "organizer", "web", "binding"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var reference = CellReference(endpoint: "cell:///ConfigurationCatalog", subscribeFeed: false, label: "configurationCatalog")
        reference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(reference)

        var elements = SkeletonElementList()
        elements.append(catalogText("Conference Demo Launcher"))
        elements.append(catalogText("Start her når du vil kjøre hele historien uten Library-søk. Hver knapp åpner en eksisterende conference-konfigurasjon i samme arbeidsrom; ingen demo-only bypasses brukes."))
        elements.append(
            catalogCardSection(
                "Live Path",
                content: [
                    dashboardKeyText("configurationCatalog.state.count"),
                    dashboardStaticText("Korteste sikre løp er public opener -> participant cockpit -> chatflate -> control tower."),
                    dashboardStaticText("Preview, profile, sponsor og identity-link holder samme designspråk som kjerneflyten. Eventuell lokal enrichment kan komme senere uten å endre denne web-stien.")
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Visual Parity Toggle",
                content: [
                    dashboardStaticText("Disse knappene viser poenget med CellConfiguration: samme cell references og samme datamodell, men to forskjellige skeleton/design-varianter i samme demo."),
                    dashboardStaticText("Bruk eksisterende-knappen for dagens canonical dashboard og Claude-knappen for warm paper/indigo/amber/green parity uten aa endre cellene bak."),
                    launcherButtonRow([
                        loadConfigurationButton("Eksisterende participant UI", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                        loadConfigurationButton("Claude participant UI", configurationName: "Conference Participant Portal Claude", sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint)
                    ]),
                    launcherButtonRow([
                        loadConfigurationButton("Eksisterende public UI", configurationName: "Conference Public Surface", sourceCellEndpoint: "cell:///ConferencePublicShell"),
                        loadConfigurationButton("Claude public UI", configurationName: "Conference Public Surface Claude", sourceCellEndpoint: "cell:///ConferencePublicShell")
                    ]),
                    launcherButtonRow([
                        loadConfigurationButton("Eksisterende organizer UI", configurationName: "Conference Control Tower", sourceCellEndpoint: "cell:///ConferenceAdminPreviewShell"),
                        loadConfigurationButton("Claude organizer UI", configurationName: "Conference Control Tower Claude", sourceCellEndpoint: "cell:///ConferenceAdminPreviewShell")
                    ]),
                    launcherButtonRow([
                        loadConfigurationButton("Eksisterende sponsor UI", configurationName: "Conference Sponsor Follow-up", sourceCellEndpoint: "cell:///ConferenceSponsorPreviewShell"),
                        loadConfigurationButton("Claude sponsor UI", configurationName: "Conference Sponsor Follow-up Claude", sourceCellEndpoint: "cell:///ConferenceSponsorPreviewShell")
                    ])
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Choose Identity Start",
                content: [
                    dashboardStaticText("For å vise forskjellen ærlig i web bruker vi to ulike requesters: en ny bruker for kaldstart og en eksisterende bruker eller demo-persona for rik conference-kontekst."),
                    dashboardStaticText("Ny entitet: logg ut og inn med en ny bruker for ekte tom entity state. Eksisterende entitet: bruk innlogget requester eller en conference demo-persona når du vil vise at relevant data allerede finnes."),
                    launcherButtonRow([
                        loadConfigurationButton("Ny entitet · onboarding", configurationName: "Conference Registration Setup", sourceCellEndpoint: "cell:///ConferenceOnboarding"),
                        loadConfigurationButton("Ny entitet · profile setup", configurationName: "Conference Public Profile Editor", sourceCellEndpoint: "cell:///ConferencePublicProfileEditorPreview")
                    ]),
                    launcherButtonRow([
                        loadConfigurationButton("Eksisterende · participant cockpit", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                        loadConfigurationButton("Eksisterende · control tower", configurationName: "Conference Control Tower", sourceCellEndpoint: "cell:///ConferenceAdminPreviewShell")
                    ])
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Act 0 · Public Opener",
                content: [
                    dashboardStaticText("Vis organizer-publisert landing, spor, sesjoner, personer og praktisk info."),
                    launcherButtonRow([
                        loadConfigurationButton("Vis public surface", configurationName: "Conference Public Surface", sourceCellEndpoint: "cell:///ConferencePublicShell"),
                        loadConfigurationButton("Gå til participant cockpit", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint)
                    ])
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Act 1 · Participant Cockpit",
                content: [
                    dashboardStaticText("Bruk dette sporet når requesteren allerede har nok conference-relevante data til å gå rett til dashboardet."),
                    dashboardStaticText("Hold deg i dashboardet til du har valgt en person, startet chat og gjort oppfølgingen synlig."),
                    launcherButtonRow([
                        loadConfigurationButton("Åpne participant cockpit", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                        loadConfigurationButton("Åpne chatflate", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch"),
                        loadConfigurationButton("Åpne full preview", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint)
                    ])
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Act 2 · Cold Start & Profile",
                content: [
                    dashboardStaticText("Bruk dette når requesteren starter med tom eller irrelevant entity state og må fylle inn conference-kontekst selv."),
                    dashboardStaticText("Vis participant-owned profile setup og publish flow, og at viewer forblir låst før publish."),
                    launcherButtonRow([
                        loadConfigurationButton("Åpne registration setup", configurationName: "Conference Registration Setup", sourceCellEndpoint: "cell:///ConferenceOnboarding"),
                        loadConfigurationButton("Åpne profile editor", configurationName: "Conference Public Profile Editor", sourceCellEndpoint: "cell:///ConferencePublicProfileEditorPreview"),
                        loadConfigurationButton("Åpne public profile", configurationName: "Conference Public Profile", sourceCellEndpoint: "cell:///ConferencePublicProfilePreview")
                    ])
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Act 3 · Organizer Perspective",
                content: [
                    dashboardStaticText("Bytt så til organizer-perspektivet og pek på den samme shared follow-up-virkeligheten, ikke på participant-private data."),
                    dashboardStaticText("Målet er å vise samme historie fra to sider: deltageren får bedre flyt, arrangøren får aggregate innsikt og bounded follow-up."),
                    launcherButtonRow([
                        loadConfigurationButton("Åpne control tower", configurationName: "Conference Control Tower", sourceCellEndpoint: "cell:///ConferenceAdminPreviewShell"),
                        loadConfigurationButton("Åpne AI-assistent", configurationName: "Conference AI Assistant", sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell")
                    ])
                ]
            )
        )

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    private static func launcherButtonRow(_ buttons: SkeletonElementList) -> SkeletonElement {
        var spacer = SkeletonSpacer()
        var spacerModifiers = SkeletonModifiers()
        spacerModifiers.height = 6
        spacer.modifiers = spacerModifiers

        return .VStack(
            SkeletonVStack(
                elements: [
                    .Spacer(spacer),
                    .HStack(SkeletonHStack(elements: buttons))
                ],
                spacing: 0
            )
        )
    }

    static func conferencePublicSurfaceConfiguration() -> CellConfiguration {
        var configuration = ConferenceShellConfigurationFactory.makePublicConfiguration()
        configuration.description = "Public conference shell for landing, registration handoff, tracks, sessions, and public-safe people/articles/facilities."
        return configuration
    }

    static func conferenceTrackDetailConfiguration() -> CellConfiguration {
        detailConfiguration(
            name: "Conference Track Detail",
            description: "Public-safe detail workspace for the currently selected conference track.",
            titleKeypath: "conferencePublicShell.state.selectedTrack.title",
            subtitleKeypath: "conferencePublicShell.state.selectedTrack.subtitle",
            detailKeypath: "conferencePublicShell.state.selectedTrack.detail",
            noteKeypath: "conferencePublicShell.state.selectedTrack.note",
            primaryButtons: [
                primaryActionButton(
                    keypath: "conferencePublicShell.startSelectedTrackHandoff",
                    label: "Klargjør spor i participant portal"
                ),
                loadConfigurationButton("Gå til registrering", configurationName: "Conference Registration Setup", sourceCellEndpoint: "cell:///ConferenceOnboarding"),
                loadConfigurationButton("Fortsett til participant portal", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                loadConfigurationButton("Tilbake til public surface", configurationName: "Conference Public Surface", sourceCellEndpoint: "cell:///ConferencePublicShell")
            ]
        )
    }

    static func conferenceSessionDetailConfiguration() -> CellConfiguration {
        detailConfiguration(
            name: "Conference Session Detail",
            description: "Public-safe detail workspace for the currently selected conference session.",
            titleKeypath: "conferencePublicShell.state.selectedSession.title",
            subtitleKeypath: "conferencePublicShell.state.selectedSession.subtitle",
            detailKeypath: "conferencePublicShell.state.selectedSession.detail",
            noteKeypath: "conferencePublicShell.state.selectedSession.note",
            primaryButtons: [
                primaryActionButton(
                    keypath: "conferencePublicShell.startSelectedSessionHandoff",
                    label: "Klargjør sesjon i participant flow"
                ),
                loadConfigurationButton("Fortsett til participant portal", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                loadConfigurationButton("Åpne participant chat", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch"),
                loadConfigurationButton("Tilbake til public surface", configurationName: "Conference Public Surface", sourceCellEndpoint: "cell:///ConferencePublicShell")
            ]
        )
    }

    static func conferenceAgendaTrackDetailConfiguration() -> CellConfiguration {
        participantAgendaDetailConfiguration(
            name: "Conference Agenda Track Detail",
            description: "Participant-owned detail workspace for the currently selected track in min agenda.",
            titleKeypath: "conferenceParticipantShell.state.program.selectedTrack.title",
            subtitleKeypath: "conferenceParticipantShell.state.program.selectedTrack.subtitle",
            detailKeypath: "conferenceParticipantShell.state.program.selectedTrack.detail",
            noteKeypath: "conferenceParticipantShell.state.program.selectedTrack.note",
            extraContent: [
                dashboardKeyText("conferenceParticipantShell.state.program.agendaSummary"),
                dashboardKeyText("conferenceParticipantShell.state.program.viewSummary"),
                dashboardKeyText("conferenceParticipantShell.state.program.timelineSummary"),
                dashboardKeyText("conferenceParticipantShell.state.program.nextAction")
            ],
            extraSections: [
                compactConferenceChatSection(
                    title: "Kompakt Chat",
                    chatKeypathPrefix: "conferenceParticipantShell.state.chat",
                    primaryButtons: [
                        loadConfigurationButton("Åpne chatflate", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch"),
                        loadConfigurationButton("Åpne full preview", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint)
                    ]
                )
            ],
            primaryButtons: [
                participantPortalActionButton(
                    "conferenceParticipantShell",
                    actionKeypath: "agenda.setView",
                    label: "Fra valgte spor",
                    payload: .object(["view": .string("focusedTracks")])
                ),
                participantPortalActionButton(
                    "conferenceParticipantShell",
                    actionKeypath: "agenda.toggleSelectedTrackFocus",
                    label: "Fokus valgt spor"
                ),
                loadConfigurationButton("Tilbake til agenda", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                loadConfigurationButton("Åpne public surface", configurationName: "Conference Public Surface", sourceCellEndpoint: "cell:///ConferencePublicShell"),
                loadConfigurationButton("Åpne track-detalj i public", configurationName: "Conference Track Detail", sourceCellEndpoint: "cell:///ConferencePublicShell")
            ]
        )
    }

    static func conferenceAgendaSessionDetailConfiguration() -> CellConfiguration {
        participantAgendaDetailConfiguration(
            name: "Conference Agenda Session Detail",
            description: "Participant-owned detail workspace for the currently selected session in min agenda.",
            titleKeypath: "conferenceParticipantShell.state.program.selectedSession.title",
            subtitleKeypath: "conferenceParticipantShell.state.program.selectedSession.subtitle",
            detailKeypath: "conferenceParticipantShell.state.program.selectedSession.detail",
            noteKeypath: "conferenceParticipantShell.state.program.selectedSession.note",
            extraContent: [
                dashboardKeyText("conferenceParticipantShell.state.sessionThread.sessionSummary"),
                dashboardKeyText("conferenceParticipantShell.state.sessionThread.participationSummary"),
                dashboardKeyText("conferenceParticipantShell.state.sessionThread.privacySummary"),
                dashboardKeyText("conferenceParticipantShell.state.sessionPolling.questionSummary"),
                dashboardKeyText("conferenceParticipantShell.state.sessionPolling.voteSummary"),
                dashboardKeyText("conferenceParticipantShell.state.sessionPolling.revealSummary")
            ],
            extraSections: [
                sessionDetailComponentsSection(title: "Koblede sesjonskomponenter"),
                sessionThreadLiveSection(
                    title: "Live sesjonschat",
                    primaryButtons: [
                        participantPortalActionButton(
                            "conferenceParticipantShell",
                            actionKeypath: "sessionThread.postMessage",
                            label: "Post i sesjonschat",
                            payload: .object(["text": .string("Spennende poeng. Hvem vil sammenligne notater etter denne sesjonen?")])
                        ),
                        participantPortalActionButton(
                            "conferenceParticipantShell",
                            actionKeypath: "sessionThread.inviteParticipants",
                            label: "Inviter Bo + Cy",
                            payload: .object([
                                "targets": .list([
                                    .object([
                                        "participantId": .string("participant-bo-demo"),
                                        "displayName": .string("Bo Demo"),
                                        "role": .string("attendee")
                                    ]),
                                    .object([
                                        "participantId": .string("participant-cy-demo"),
                                        "displayName": .string("Cy Demo"),
                                        "role": .string("speaker")
                                    ])
                                ])
                            ])
                        ),
                        participantPortalActionButton(
                            "conferenceParticipantShell",
                            actionKeypath: "sessionThread.acceptInvitation",
                            label: "Bli med i tråd"
                        ),
                        loadConfigurationButton("Åpne full preview", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint)
                    ]
                ),
                compactConferenceChatSection(
                    title: "Kompakt Chat",
                    chatKeypathPrefix: "conferenceParticipantShell.state.chat",
                    primaryButtons: [
                        loadConfigurationButton("Åpne chatflate", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch"),
                        loadConfigurationButton("Åpne full preview", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint)
                    ]
                )
            ],
            primaryButtons: [
                participantPortalActionButton(
                    "conferenceParticipantShell",
                    actionKeypath: "agenda.prepareSelectedSessionContext",
                    label: "Klargjør session thread"
                ),
                participantPortalActionButton(
                    "conferenceParticipantShell",
                    actionKeypath: "agenda.toggleSelectedSessionSaved",
                    label: "Lagre/fjern valgt"
                ),
                loadConfigurationButton("Åpne participant chat", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch"),
                loadConfigurationButton("Åpne full preview", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                loadConfigurationButton("Åpne sesjonsdetalj i public", configurationName: "Conference Session Detail", sourceCellEndpoint: "cell:///ConferencePublicShell"),
                loadConfigurationButton("Tilbake til agenda", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint)
            ],
            includeSessionThreadLiveReference: true
        )
    }

    static func conferenceFeaturedPersonDetailConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Conference Featured Person Detail")
        configuration.description = "Public-safe detail workspace for the currently selected featured person, with a safe handoff into participant-owned chat."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferencePublicShell",
            sourceCellName: "ConferencePublicShellCell",
            purpose: "Conference Featured Person Detail",
            purposeDescription: "Public-safe featured-person detail that can hand off into participant-owned chat only for the demo people whose participant IDs are already modeled.",
            interests: ["conference", "public", "detail", "featured-person", "chat-handoff", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var publicReference = CellReference(endpoint: "cell:///ConferencePublicShell", subscribeFeed: false, label: "conferencePublicShell")
        publicReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(publicReference)

        var chatReference = CellReference(endpoint: "cell:///ConferenceChatLaunch", subscribeFeed: false, label: "conferenceChat")
        chatReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(chatReference)

        var elements = SkeletonElementList()
        elements.append(catalogText("Conference Featured Person Detail"))
        elements.append(
            catalogCardSection(
                "Detail",
                content: [
                    dashboardKeyText("conferencePublicShell.state.selectedPerson.title"),
                    dashboardKeyText("conferencePublicShell.state.selectedPerson.subtitle"),
                    dashboardKeyText("conferencePublicShell.state.selectedPerson.detail"),
                    dashboardKeyText("conferencePublicShell.state.selectedPerson.note"),
                    dashboardKeyText("conferencePublicShell.state.selectedPerson.chatSummary"),
                    .HStack(
                        SkeletonHStack(elements: [
                            loadConfigurationButton("Gå til participant portal", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                            loadConfigurationButton("Tilbake til public surface", configurationName: "Conference Public Surface", sourceCellEndpoint: "cell:///ConferencePublicShell")
                        ])
                    )
                ]
            )
        )
        elements.append(
            compactConferenceChatSection(
                title: "Kompakt Chat",
                chatKeypathPrefix: "conferenceChat.state",
                primaryButtons: [
                    primaryActionButton(
                        keypath: "conferencePublicShell.startSelectedPersonChat",
                        label: "Start chat med featured person"
                    ),
                    loadConfigurationButton("Åpne participant chat", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch")
                ]
            )
        )
        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func conferenceParticipantPortalPreviewConfiguration() -> CellConfiguration {
        var configuration = ConferenceShellConfigurationFactory.makeParticipantConfiguration()
        configuration.name = "Conference Participant Portal Preview"
        configuration.description = "Full preview-wrapper over ConferenceParticipantShell for access, onboarding, session thread, polling, meetings og shared relations."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
            sourceCellName: "ConferenceParticipantPreviewShellCell",
            purpose: "Conference participantportal preview",
            purposeDescription: "Full participant-shell gjennom en stabil preview-wrapper, slik at hele den utvidede conference-flaten kan kjøres i web Library uten eier-auth shortcuts.",
            interests: ["conference", "participant", "preview", "onboarding", "access", "sessions", "polling", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        if var references = configuration.cellReferences, references.isEmpty == false {
            references[0].endpoint = "cell:///ConferenceParticipantPreviewShell"
            references[0].subscribeFeed = false
            configuration.cellReferences = references
        }

        return appendingSection(
            catalogCardSection(
                "Demo Flow",
                content: [
                    dashboardStaticText("Bruk denne utvidede flaten når du vil se onboarding, access, session og polling-ground truth uten å forlate conference-designet."),
                    .HStack(
                        SkeletonHStack(elements: [
                            loadConfigurationButton("Åpne participant cockpit", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                            loadConfigurationButton("Åpne profile editor", configurationName: "Conference Public Profile Editor", sourceCellEndpoint: "cell:///ConferencePublicProfileEditorPreview"),
                            loadConfigurationButton("Åpne public profile", configurationName: "Conference Public Profile", sourceCellEndpoint: "cell:///ConferencePublicProfilePreview")
                        ])
                    )
                ]
            ),
            to: configuration
        )
    }

    static func conferenceRegistrationSetupConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Conference Registration Setup")
        configuration.description = "Cold-start workspace for participant-owned conference registration, profile setup, consent choices, and optional payment preparation."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferenceOnboarding",
            sourceCellName: "ConferenceOnboardingCell",
            purpose: "Conference registration setup",
            purposeDescription: "Cold-start workspace for participant-owned conference registration, profile setup, consent choices, and optional payment prep before entering the participant cockpit.",
            interests: ["conference", "registration", "onboarding", "profile", "consent", "payments", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var onboardingReference = CellReference(endpoint: "cell:///ConferenceOnboarding", subscribeFeed: false, label: "conferenceOnboarding")
        onboardingReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(onboardingReference)

        var profileReference = CellReference(endpoint: "cell:///ConferencePublicProfileEditorPreview", subscribeFeed: false, label: "conferencePublicProfileEditor")
        profileReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(profileReference)

        var paymentReference = CellReference(endpoint: "cell:///PaymentGate", subscribeFeed: false, label: "paymentGate")
        paymentReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(paymentReference)

        var aiReference = CellReference(endpoint: "cell:///ConferenceAIGatewayPreview", subscribeFeed: false, label: "registrationAI")
        aiReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(aiReference)

        let registrationSystemPrompt = """
        You are a conference registration draft assistant. Suggest profile text, purpose labels, interest labels, and consent questions based only on the visible participant-owned setup fields in this workspace. Never assume consent has been granted. Never claim data has been stored. Produce concise drafts that the participant can review and copy manually before saving.
        """

        var elements = SkeletonElementList()
        elements.append(catalogText("Conference Registration Setup"))
        elements.append(catalogText("Bruk denne flaten når requesteren starter uten nok conference-relevant entity data. Profil, purpose, samtykke og publiserbar profil forblir participant-owned hele veien."))
        elements.append(
            catalogCardSection(
                "Readiness",
                content: [
                    dashboardKeyText("conferenceOnboarding.state.headline"),
                    dashboardKeyText("conferenceOnboarding.state.intro"),
                    dashboardKeyText("conferenceOnboarding.state.profileSummary"),
                    dashboardKeyText("conferenceOnboarding.state.conferenceSummary"),
                    dashboardKeyText("conferenceOnboarding.state.saveStatus"),
                    dashboardKeyText("conferenceOnboarding.state.storageSummary"),
                    dashboardStaticText("Denne cold-starten skriver bare participant-owned truth under entity anchor. Arrangøren ser senere bare aggregate eller agreement-bundet data.")
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Participant-Owned Basics",
                content: [
                    dashboardKeyText("conferenceOnboarding.state.subscriptions.identityProfile.state.name"),
                    dashboardKeyText("conferenceOnboarding.state.subscriptions.identityProfile.state.company"),
                    dashboardKeyText("conferenceOnboarding.state.subscriptions.identityProfile.state.email"),
                    dashboardKeyText("conferenceOnboarding.state.subscriptions.identityProfile.state.role"),
                    dashboardStaticText("Denne første versjonen bruker trygge presets og tilgrensende conference-flater for full kontroll, i stedet for å innføre nye onboarding-drafts i cellene."),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(
                                keypath: "conferenceOnboarding.upsertProfile",
                                label: "Bruk deltagerprofil",
                                payload: .object([
                                    "name": .string("New conference participant"),
                                    "company": .string("Independent attendee"),
                                    "role": .string("attendee")
                                ])
                            ),
                            primaryActionButton(
                                keypath: "conferenceOnboarding.upsertProfile",
                                label: "Bruk partnerprofil",
                                payload: .object([
                                    "name": .string("Conference partner"),
                                    "company": .string("Partner organization"),
                                    "role": .string("attendee")
                                ])
                            ),
                            primaryActionButton(
                                keypath: "conferenceOnboarding.upsertProfile",
                                label: "Lagre nåværende profil",
                                payload: .object([:])
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            loadConfigurationButton("Åpne participant preview", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                            loadConfigurationButton("Open Entity Studio", configurationName: "Entity Studio", sourceCellEndpoint: "cell:///EntityStudio")
                        ])
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "AI Draft Companion",
                content: [
                    dashboardStaticText("AI-forslagene er en trygg sidevogn i denne flaten. Assistenten får lage utkast til profiltekst, purpose og interests, men ingenting skrives til entity anchor før du selv lagrer via onboarding eller profile editor."),
                    dashboardKeyText("registrationAI.state.setup.statusLabel"),
                    dashboardKeyText("registrationAI.state.setup.nextStep"),
                    dashboardKeyText("registrationAI.state.lastInvocation.outputPreview"),
                    dashboardKeyText("registrationAI.state.lastInvocation.model"),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(
                                keypath: "registrationAI.applyDraftProfile",
                                label: "Hosted API",
                                payload: .object([
                                    "providerID": .string("openai-compatible"),
                                    "model": .string("gpt-4.1-mini"),
                                    "requiresAPIKey": .bool(true),
                                    "cachePolicy": .string("useCache")
                                ])
                            ),
                            primaryActionButton(
                                keypath: "registrationAI.setDraftSystemPrompt",
                                label: "Load registration prompt",
                                payload: .string(registrationSystemPrompt)
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(
                                keypath: "registrationAI.setDraftPrompt",
                                label: "Draft cold-start profile",
                                payload: .string("Using the visible conference onboarding state, draft a short participant profile, a public headline, and a short bio for someone arriving with almost no relevant entity data. Keep it privacy-first and explicitly list what still needs the participant's confirmation.")
                            ),
                            primaryActionButton(
                                keypath: "registrationAI.setDraftPrompt",
                                label: "Draft purpose & interests",
                                payload: .string("Using the visible onboarding state, suggest 3 purpose labels and 5 interest labels for this participant. Keep them concrete, conference-relevant, and easy to confirm manually.")
                            ),
                            primaryActionButton(
                                keypath: "registrationAI.setDraftPrompt",
                                label: "Draft consent questions",
                                payload: .string("Based on the visible onboarding and profile context, draft a short privacy-first checklist that helps the participant decide what to share, what to keep private, and what only to expose as aggregate or agreement-bound data.")
                            )
                        ])
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "registrationAI.state.draft.model",
                            targetKeypath: "registrationAI.setDraftModel",
                            placeholder: "Model"
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "registrationAI.state.draft.prompt",
                            targetKeypath: "registrationAI.setDraftPrompt",
                            placeholder: "Be AI draft profile copy, purpose labels, interests, or a consent checklist. Review manually before you save anything.",
                            minLines: 5,
                            maxLines: 12,
                            submitOnEnter: false,
                            editorMode: .plain
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(keypath: "registrationAI.invokeDraft", label: "Generate draft"),
                            primaryActionButton(keypath: "registrationAI.clearDraftAPIKey", label: "Clear session key"),
                            loadConcreteConfigurationButton("Åpne full AI assistant", configuration: conferenceAIAssistantConfiguration())
                        ])
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Purpose, Interests & Consent",
                content: [
                    dashboardStaticText("Velg et kaldstart-preset, juster samtykke eksplisitt, og bekreft deretter hva som faktisk er lagret i entityen."),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferenceOnboarding.state.purposes",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferenceOnboarding.state.interests",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferenceOnboarding.state.consents",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferenceOnboarding.state.visibilityPolicies",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(
                                keypath: "conferenceOnboarding.saveSnapshot",
                                label: "Preset · partnering",
                                payload: .object([
                                    "purposes": .list([
                                        .object(["label": .string("Find implementation partners"), "weight": .float(0.92)]),
                                        .object(["label": .string("Meet relevant peers"), "weight": .float(0.78)])
                                    ]),
                                    "interests": .list([
                                        .object(["label": .string("Federated identity"), "weight": .float(0.88)]),
                                        .object(["label": .string("Agent governance"), "weight": .float(0.79)])
                                    ])
                                ])
                            ),
                            primaryActionButton(
                                keypath: "conferenceOnboarding.saveSnapshot",
                                label: "Preset · learning",
                                payload: .object([
                                    "purposes": .list([
                                        .object(["label": .string("Learn privacy patterns"), "weight": .float(0.89)]),
                                        .object(["label": .string("Bring ideas home"), "weight": .float(0.71)])
                                    ]),
                                    "interests": .list([
                                        .object(["label": .string("Sovereign tech"), "weight": .float(0.83)]),
                                        .object(["label": .string("Procurement"), "weight": .float(0.62)])
                                    ])
                                ])
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(
                                keypath: "conferenceOnboarding.setConsent",
                                label: "Toggle sponsor insights",
                                payload: .object(["purpose": .string("sponsorInsights")])
                            ),
                            primaryActionButton(
                                keypath: "conferenceOnboarding.setConsent",
                                label: "Toggle lead capture",
                                payload: .object(["purpose": .string("leadCapture")])
                            ),
                            primaryActionButton(
                                keypath: "conferenceOnboarding.setFieldVisibility",
                                label: "Company -> aggregated",
                                payload: .object([
                                    "field": .string("company"),
                                    "level": .string("aggregatedOnly")
                                ])
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(
                                keypath: "conferenceOnboarding.setFieldVisibility",
                                label: "Email -> private",
                                payload: .object([
                                    "field": .string("email"),
                                    "level": .string("private")
                                ])
                            ),
                            primaryActionButton(
                                keypath: "conferenceOnboarding.setFieldVisibility",
                                label: "Purpose -> shared",
                                payload: .object([
                                    "field": .string("purposeSummary"),
                                    "level": .string("shared")
                                ])
                            )
                        ])
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Build Your Public Profile",
                content: [
                    dashboardStaticText("Dette er den delen av cold-starten som handler om hva andre faktisk skal kunne se. Først skriver du utkastet ditt, deretter velger du synlige felt, og til slutt publiserer du når du er komfortabel."),
                    dashboardStaticText("Steg 1: bygg et trygt utkast som fortsatt bare tilhører deg."),
                    dashboardKeyText("conferencePublicProfileEditor.state.workspace.title"),
                    dashboardKeyText("conferencePublicProfileEditor.state.workspace.nextStep"),
                    dashboardKeyText("conferencePublicProfileEditor.state.publicationSummary"),
                    dashboardKeyText("conferencePublicProfileEditor.state.configurationSummary"),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "conferencePublicProfileEditor.state.title",
                            targetKeypath: "conferencePublicProfileEditor.setTitle",
                            placeholder: "Profile title"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "conferencePublicProfileEditor.state.headline",
                            targetKeypath: "conferencePublicProfileEditor.setHeadline",
                            placeholder: "Short public headline"
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "conferencePublicProfileEditor.state.staticBio",
                            targetKeypath: "conferencePublicProfileEditor.setStaticBio",
                            placeholder: "Short public bio shown if you publish the profile",
                            minLines: 4,
                            maxLines: 8,
                            submitOnEnter: false,
                            editorMode: .plain
                        )
                    ),
                    dashboardStaticText("Bilde er fortsatt participant-owned. Legg inn en trygg URL eller asset reference her; den blir ikke synlig for andre før profilen faktisk publiseres."),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "conferencePublicProfileEditor.state.imageReference",
                            targetKeypath: "conferencePublicProfileEditor.setImageReference",
                            placeholder: "Image URL or asset reference"
                        )
                    ),
                    dashboardStaticText("Steg 2: velg nøyaktig hvilke felt som faktisk skal være synlige."),
                    dashboardKeyText("conferencePublicProfileEditor.state.visibleFieldSummary"),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferencePublicProfileEditor.state.sourceFields",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferencePublicProfileEditor.state.visibleFields",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(keypath: "conferencePublicProfileEditor.createProfileVariant", label: "Create variant"),
                            primaryActionButton(
                                keypath: "conferencePublicProfileEditor.toggleVisibleField",
                                label: "Toggle company",
                                payload: .object(["field": .string("company")])
                            ),
                            primaryActionButton(
                                keypath: "conferencePublicProfileEditor.toggleVisibleField",
                                label: "Toggle purpose",
                                payload: .object(["field": .string("purposeSummary")])
                            )
                        ])
                    ),
                    dashboardStaticText("Steg 3: bruk viewer-forhåndsvisningen som sannheten for hva andre vil se."),
                    dashboardStaticText("Se alltid viewer-versjonen før du publiserer. Det er den andre faktisk ser, ikke editoren."),
                    dashboardKeyText("conferencePublicProfileEditor.state.preview.workspace.title"),
                    dashboardKeyText("conferencePublicProfileEditor.state.preview.workspace.publicationBadge"),
                    dashboardKeyText("conferencePublicProfileEditor.state.preview.profile.displayName"),
                    dashboardKeyText("conferencePublicProfileEditor.state.preview.profile.headline"),
                    dashboardKeyText("conferencePublicProfileEditor.state.preview.profile.contactSummary"),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferencePublicProfileEditor.state.preview.badges",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferencePublicProfileEditor.state.preview.focusAreas",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(keypath: "conferencePublicProfileEditor.publishProfile", label: "Publish profile"),
                            primaryActionButton(keypath: "conferencePublicProfileEditor.unpublishProfile", label: "Unpublish profile"),
                            loadConfigurationButton("Åpne public profile", configurationName: "Conference Public Profile", sourceCellEndpoint: "cell:///ConferencePublicProfilePreview"),
                            loadConcreteConfigurationButton("Åpne AI draft companion", configuration: conferenceAIAssistantConfiguration())
                        ])
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Microtransaction Prep",
                content: [
                    dashboardStaticText("Betaling er bare synlig i denne runden. Den er ikke en hard gate for å komme inn i demoen."),
                    dashboardKeyText("paymentGate.state.currency"),
                    dashboardKeyText("paymentGate.state.defaultPriceMinorUnits"),
                    dashboardKeyText("paymentGate.state.resourceCount"),
                    dashboardKeyText("paymentGate.state.receiptCount"),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "paymentGate.state.resources",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            loadConfigurationButton("Åpne payment gate", configurationName: "Payment Gate", sourceCellEndpoint: "cell:///PaymentGate"),
                            loadConfigurationButton("Tilbake til public surface", configurationName: "Conference Public Surface", sourceCellEndpoint: "cell:///ConferencePublicShell"),
                            loadConfigurationButton("Gå til participant cockpit", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint)
                        ])
                    )
                ]
            )
        )

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func conferenceParticipantChatConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Conference Participant Chat")
        configuration.description = "Eksplisitt chat-workbench for selected-person til chat til follow-up, bygget direkte på ConferenceChatLaunch."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferenceChatLaunch",
            sourceCellName: "ConferenceChatLaunchCell",
            purpose: "Conference participant chat",
            purposeDescription: "Explicit participant chat surface for discovery follow-up, message proof of life og meeting ask, uten å late som chat er organizer-owned state.",
            interests: ["conference", "participant", "chat", "follow-up", "shared-relations", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var reference = CellReference(endpoint: "cell:///ConferenceChatLaunch", subscribeFeed: false, label: "conferenceChat")
        reference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(reference)
        var participantReference = CellReference(endpoint: "cell:///ConferenceParticipantPreviewShell", subscribeFeed: false, label: "conferenceParticipantShell")
        participantReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(participantReference)

        var elements = SkeletonElementList()
        elements.append(
            catalogCardSection(
                "Conference Participant Chat",
                content: [
                    dashboardKeyText("conferenceChat.state.headline"),
                    dashboardKeyText("conferenceChat.state.conversationSummary"),
                    dashboardKeyText("conferenceChat.state.status"),
                    .HStack(
                        SkeletonHStack(elements: [
                            .Button(
                                SkeletonButton(
                                    keypath: "conferenceChat.startChat",
                                    label: "Start demo-chat med Sara",
                                    payload: ValueType.object([
                                        "source": .string("participant-chat-surface"),
                                        "targets": .list([
                                            .object([
                                                "participantId": .string("participant-102"),
                                                "displayName": .string("Sara M."),
                                                "company": .string("Cell-native Privacy"),
                                                "role": .string("speaker")
                                            ])
                                        ])
                                    ])
                                )
                            ),
                            loadConfigurationButton(
                                "Tilbake til portal",
                                configurationName: Self.conferenceParticipantPortalLoadConfigurationName,
                                sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint
                            )
                        ])
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Deltakere",
                content: [
                    dashboardKeyText("conferenceChat.state.participantsSummary"),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferenceChat.state.participants",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Inviter flere",
                content: [
                    dashboardKeyText("conferenceChat.state.membership.nextAction"),
                    dashboardStaticText("Midlertidig trygg demo-handling: foreslå Samir som nytt medlem. Eieren må fortsatt godkjenne forespørselen."),
                    .HStack(
                        SkeletonHStack(elements: [
                            .Button(
                                SkeletonButton(
                                    keypath: "conferenceChat.requestMemberInvite",
                                    label: "Foreslå Samir",
                                    payload: ValueType.object([
                                        "targets": .list([
                                            .object([
                                                "participantId": .string("participant-188"),
                                                "displayName": .string("Samir Iqbal"),
                                                "company": .string("Open Civic Labs"),
                                                "role": .string("organizer")
                                            ])
                                        ])
                                    ])
                                )
                            ),
                            .Button(
                                SkeletonButton(
                                    keypath: "conferenceChat.approveFirstMemberInvite",
                                    label: "Godkjenn første medlem",
                                    payload: ValueType.object([:])
                                )
                            )
                        ])
                    ),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferenceChat.state.pendingMemberRequests",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Meldinger",
                content: [
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferenceChat.state.messages",
                            flowElementSkeleton: dashboardMessageRowSkeleton()
                        )
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Skriv melding",
                content: [
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "conferenceChat.state.editor.draft",
                            targetKeypath: "conferenceChat.setDraft",
                            placeholder: "Skriv en konferansemelding",
                            minLines: 3,
                            maxLines: 8,
                            submitOnEnter: false,
                            editorMode: .plain
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            .Button(
                                SkeletonButton(
                                    keypath: "conferenceChat.sendMessage",
                                    label: "Send melding",
                                    payload: ValueType.object([:])
                                )
                            ),
                            .Button(
                                SkeletonButton(
                                    keypath: "conferenceChat.setDraft",
                                    label: "Tøm utkast",
                                    payload: ValueType.object(["text": .string("")])
                                )
                            )
                        ])
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Chat-verktøy",
                content: [
                    dashboardKeyText("conferenceParticipantShell.state.concierge.toolBoundary"),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "conferenceParticipantShell.state.concierge.toolCards",
                            flowElementSkeleton: conferenceParticipantPortalToolCardRowSkeleton()
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            participantPortalActionButton(
                                "conferenceParticipantShell",
                                actionKeypath: "concierge.applyToolCard",
                                label: "Lag notatutkast",
                                payload: .object(["toolId": .string("draft-note")])
                            ),
                            participantPortalActionButton(
                                "conferenceParticipantShell",
                                actionKeypath: "concierge.applyToolCard",
                                label: "Start prosjektutkast",
                                payload: .object(["toolId": .string("start-project")])
                            ),
                            participantPortalActionButton(
                                "conferenceParticipantShell",
                                actionKeypath: "concierge.applyToolCard",
                                label: "Finn delt lokasjon",
                                payload: .object(["toolId": .string("find-peer-location")])
                            ),
                            participantPortalActionButton(
                                "conferenceParticipantShell",
                                actionKeypath: "concierge.dismissToolCard",
                                label: "Skjul nearby-forslag",
                                payload: .object(["toolId": .string("nearby-invite")])
                            )
                        ])
                    ),
                    dashboardKeyText("conferenceParticipantShell.state.concierge.lastActionSummary")
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Chat-innstillinger",
                content: [
                    dashboardKeyText("conferenceChat.state.membership.summary"),
                    .HStack(
                        SkeletonHStack(elements: [
                            .Button(
                                SkeletonButton(
                                    keypath: "conferenceChat.setMemberExpansionPolicy",
                                    label: "Tillat nye medlemmer",
                                    payload: ValueType.object(["allowed": .bool(true)])
                                )
                            ),
                            .Button(
                                SkeletonButton(
                                    keypath: "conferenceChat.setMemberExpansionPolicy",
                                    label: "Stans nye medlemmer",
                                    payload: ValueType.object(["allowed": .bool(false)])
                                )
                            )
                        ])
                    )
                ]
            )
        )
        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func conferenceNearbyRadarConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Conference Nearby Radar")
        configuration.description = "Capability-gated nearby participant workbench over ConferenceParticipantShell discovery state."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
            sourceCellName: "ConferenceParticipantPreviewShellCell",
            purpose: "Conference nearby radar",
            purposeDescription: "Portable nearby/radar surface for scanner-projected encounters. Binding can feed real scanner rows; web and staging remain quiet when capability is absent.",
            interests: ["conference", "participant", "nearby", "radar", "scanner", "discovery", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var reference = CellReference(endpoint: "cell:///ConferenceParticipantPreviewShell", subscribeFeed: false, label: "conferenceParticipantShell")
        reference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(reference)

        let referenceLabel = "conferenceParticipantShell"
        let elements: SkeletonElementList = [
            catalogCardSection(
                "Conference Nearby Radar",
                content: [
                    dashboardKeyText("\(referenceLabel).state.discovery.nearby.status"),
                    dashboardKeyText("\(referenceLabel).state.discovery.nearby.fallback"),
                    dashboardKeyText("\(referenceLabel).state.discovery.alignmentSummary"),
                    .HStack(
                        SkeletonHStack(elements: [
                            loadConfigurationButton("Åpne people-flaten", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                            loadConfigurationButton("Åpne chatflate", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch")
                        ])
                    )
                ]
            ),
            catalogCardSection(
                "Nearby encounters",
                content: [
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "\(referenceLabel).state.discovery.nearby.encounters",
                            flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: true)
                        )
                    )
                ]
            ),
            catalogCardSection(
                "Resolved people",
                content: [
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "\(referenceLabel).state.discovery.candidates",
                            flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: true)
                        )
                    ),
                    dashboardStaticText("Valgt kontakt", fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                    dashboardKeyText("\(referenceLabel).state.discovery.selectionSummary"),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "\(referenceLabel).state.discovery.selectedActions",
                            flowElementSkeleton: dashboardDiscoveryRowSkeleton()
                        )
                    )
                ]
            )
        ]
        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func conferenceControlTowerConfiguration() -> CellConfiguration {
        var configuration = ConferenceShellConfigurationFactory.makeAdminConfiguration()
        configuration.description = "Organizer control tower som er admin-siden av samme demo-historie som Conference Participant Portal Dashboard. Preview-wrapperen peker til den faktiske ConferenceAdminShell-kontrakten, slik at publisert content, operations, insights, simulation og sponsor follow-up holder seg i parity mellom web, staging og Binding."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferenceAdminPreviewShell",
            sourceCellName: "ConferenceAdminPreviewShellCell",
            purpose: "Conference control tower",
            purposeDescription: "Organizer-siden av conference-demoen. Denne flaten viser hvordan participant onboarding, programvalg, møter, innsikter og sponsor-signaler samles i ett control tower uten å gå utenom den faktiske ConferenceAdminShell-kontrakten.",
            interests: ["conference", "organizer", "admin", "control-tower", "insights", "simulation", "publishing", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )
        return appendingSection(
            catalogCardSection(
                "Demo Flow",
                content: [
                    dashboardStaticText("Bruk først seksjonen Same Conference Reality, og gå deretter til Organizer Insight Story før du åpner access, content, insights og sponsor."),
                    dashboardStaticText("Organizer ser aggregate/projection, agreement-vinduer og sponsor-safe views, ikke participant-private slices."),
                    .HStack(
                        SkeletonHStack(elements: [
                            loadConfigurationButton("Åpne participant cockpit", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                            loadConfigurationButton("Åpne demo launcher", configurationName: "Conference Demo Launcher", sourceCellEndpoint: "cell:///ConfigurationCatalog")
                        ])
                    )
                ]
            ),
            to: configuration
        )
    }

    static func scaffoldSetupConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Scaffold Setup & Identity Link")
        configuration.description = "Admin workspace for first-run scaffold bootstrap and the next safe identity-link step between web and phone."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ScaffoldSetup",
            sourceCellName: "ScaffoldSetupCell",
            purpose: "Scaffold setup og identity linking",
            purposeDescription: "Vis scaffold-owner status, bootstrap en stabil owner ved første installasjon, og bruk samme flate som ærlig startpunkt for senere same-entity linking mellom web og Binding.",
            interests: ["scaffold", "setup", "bootstrap", "identity", "linking", "admin", "proofs", "web"],
            menuSlots: []
        )

        var setupReference = CellReference(endpoint: "cell:///ScaffoldSetup", subscribeFeed: false, label: "scaffoldSetup")
        setupReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(setupReference)

        var entryReference = CellReference(
            endpoint: AdminControlPlaneRouting.current.endpoint(for: "AdminEntry"),
            subscribeFeed: false,
            label: "adminEntry"
        )
        entryReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(entryReference)

        var elements = SkeletonElementList()
        elements.append(catalogText("Scaffold Setup & Identity Link"))
        elements.append(catalogText("Denne flaten er for produksjonsnær førstegangsoppsett: bootstrap scaffold owner først, og bruk så samme workspace til å forklare og senere drive trygg linking mellom web-identitet og telefon-identitet."))
        elements.append(
            catalogCardSection(
                "Owner Status",
                content: [
                    dashboardKeyText("scaffoldSetup.state.statusBadge"),
                    dashboardKeyText("scaffoldSetup.state.bootstrapStatus"),
                    dashboardKeyText("scaffoldSetup.state.bootstrap.recommendedNextAction"),
                    dashboardKeyText("scaffoldSetup.state.entryStatus"),
                    dashboardKeyText("scaffoldSetup.state.ownerSummary"),
                    dashboardKeyText("scaffoldSetup.state.owner.ownerContext"),
                    dashboardKeyText("scaffoldSetup.state.owner.resolutionSource"),
                    dashboardKeyText("scaffoldSetup.state.owner.identityUUID"),
                    dashboardKeyText("scaffoldSetup.state.owner.displayName"),
                    dashboardKeyText("scaffoldSetup.state.owner.publicSigningKey"),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(keypath: "scaffoldSetup.refresh", label: "Oppdater status"),
                            primaryActionButton(keypath: "scaffoldSetup.bootstrapOwner", label: "Bootstrap scaffold owner")
                        ])
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Admin Entry",
                content: [
                    dashboardStaticText("Tilgang kommer fra eksplisitt admin entry-proof og senere agreements, ikke fra at denne konfigurasjonen finnes i Library."),
                    dashboardKeyText("adminEntry.state.policy.proofKeypath"),
                    dashboardKeyText("adminEntry.state.policy.agreementConditionStatement"),
                    dashboardKeyText("adminEntry.state.policy.allowScaffoldOwnerIssuer"),
                    dashboardKeyText("adminEntry.state.policy.allowTrustedIssuers"),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "adminEntry.state.trustedIssuers",
                            flowElementSkeleton: adminIssuerRowSkeleton()
                        )
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Identity Linking",
                content: [
                    dashboardKeyText("scaffoldSetup.state.identityLinking.status"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.challengeSummary"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.pendingChallengesSummary"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.challengeHistorySummary"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.activeLinksSummary"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.currentChallengeStatus"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.sameEntityRule"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.qrRule"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.grantRule"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.recommendedFlow"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.currentChallengeReference"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.payloadSummary"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.transportSummary"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.transportBoundary.status"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.transportBoundary.guidance"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.authorityBoundary.status"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.authorityBoundary.guidance"),
                    catalogRenderedHTML("scaffoldSetup.state.identityLinking.currentChallengeRenderedHTML"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.currentChallengeTransportURL"),
                    dashboardKeyText("scaffoldSetup.state.identityLinking.currentChallengePayload"),
                    .HStack(
                        SkeletonHStack(elements: [
                            primaryActionButton(keypath: "scaffoldSetup.createLinkChallenge", label: "Lag link challenge"),
                            primaryActionButton(keypath: "scaffoldSetup.approveCurrentLinkChallenge", label: "Godkjenn aktiv challenge")
                        ])
                    ),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "scaffoldSetup.state.identityLinking.pendingChallenges",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "scaffoldSetup.state.identityLinking.challengeHistory",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "scaffoldSetup.state.identityLinking.activeLinks",
                            flowElementSkeleton: dashboardConnectionRowSkeleton()
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            loadConfigurationButton("Open Agreement Workbench", configurationName: "Agreement Workbench", sourceCellEndpoint: "cell:///AgreementWorkbench"),
                            loadConfigurationButton("Open Participation Hub", configurationName: "Participation Hub", sourceCellEndpoint: "cell:///ParticipationHub"),
                            loadConfigurationButton("Open Entity Studio", configurationName: "Entity Studio", sourceCellEndpoint: "cell:///EntityStudio")
                        ])
                    )
                ]
            )
        )
        elements.append(
            catalogCardSection(
                "Role Grant Boundary",
                content: [
                    dashboardKeyText("scaffoldSetup.state.roleGranting.status"),
                    dashboardKeyText("scaffoldSetup.state.roleGranting.guidance"),
                    dashboardKeyText("scaffoldSetup.state.roleGranting.acceptedLinkCount")
                ]
            )
        )

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func conferencePublicProfileEditorConfiguration() -> CellConfiguration {
        var configuration = ConferencePublicProfileConfigurationFactory.makeEditorConfiguration(
            endpoint: "cell:///ConferencePublicProfileEditorPreview",
            sourceCellName: "ConferencePublicProfileEditorPreviewCell",
            referenceLabel: "conferencePublicProfileEditor"
        )
        configuration.description = "Participant-owned editor for selecting which conference profile data to expose, including static text and image reference."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferencePublicProfileEditorPreview",
            sourceCellName: "ConferencePublicProfileEditorPreviewCell",
            purpose: "Conference public profile editor",
            purposeDescription: "Participant tool for composing a shareable conference profile from participant-owned entity truth and visibility choices.",
            interests: ["conference", "profile", "participant", "editor", "visibility", "sharing", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )
        return appendingSection(
            catalogCardSection(
                "Demo Flow",
                content: [
                    dashboardStaticText("Publisering her er participant-owned. Viewer forblir låst før publish."),
                    .HStack(
                        SkeletonHStack(elements: [
                            loadConfigurationButton("Åpne public profile", configurationName: "Conference Public Profile", sourceCellEndpoint: "cell:///ConferencePublicProfilePreview"),
                            loadConfigurationButton("Tilbake til portalen", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint)
                        ])
                    )
                ]
            ),
            to: configuration
        )
    }

    static func conferencePublicProfileConfiguration() -> CellConfiguration {
        var configuration = ConferencePublicProfileConfigurationFactory.makeViewerConfiguration(
            endpoint: "cell:///ConferencePublicProfilePreview",
            sourceCellName: "ConferencePublicProfilePreviewCell",
            referenceLabel: "conferencePublicProfileViewer"
        )
        configuration.description = "Viewer-facing conference profile card generated from the participant-owned public-profile slice."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferencePublicProfilePreview",
            sourceCellName: "ConferencePublicProfilePreviewCell",
            purpose: "Conference public profile",
            purposeDescription: "Conference-facing profile card that shows only the fields the participant has selected and published.",
            interests: ["conference", "profile", "viewer", "directory", "sharing", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )
        return appendingSection(
            catalogCardSection(
                "Demo Flow",
                content: [
                    dashboardStaticText("Hvis denne fortsatt er låst, er det et ærlig tegn på at profilen ikke er publisert ennå."),
                    .HStack(
                        SkeletonHStack(elements: [
                            loadConfigurationButton("Tilbake til portalen", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                            loadConfigurationButton("Åpne control tower", configurationName: "Conference Control Tower", sourceCellEndpoint: "cell:///ConferenceAdminPreviewShell")
                        ])
                    )
                ]
            ),
            to: configuration
        )
    }

    static func conferenceAIAssistantConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Conference AI Assistant")
        configuration.description = "Konferansecopilot som kombinerer participant preview-state med AIGateway for briefing, matchmaking og møteoppfølging i samme arbeidsflate."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
            sourceCellName: "ConferenceParticipantPreviewShellCell",
            purpose: "Conference copilot",
            purposeDescription: "Kombiner participant-shellens levende kontekst med embedded AIGateway for briefing, prioritering, matchmaking og follow-up uten å forlate samme skeleton.",
            interests: ["conference", "ai", "copilot", "participant", "matchmaking", "meetings", "prompting", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var conferenceReference = CellReference(endpoint: "cell:///ConferenceParticipantPreviewShell", subscribeFeed: false, label: "conferenceParticipantShell")
        conferenceReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(conferenceReference)

        var aiReference = CellReference(endpoint: "cell:///ConferenceAIGatewayPreview", label: "aiGateway")
        aiReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(aiReference)

        let conferenceSystemPrompt = """
        You are a conference copilot. Use only the participant context visible in this workspace. Stay concrete, concise, and action-oriented. Prioritize the next sessions, the best people to meet, and the shortest path to meaningful follow-up.
        """

        var elements = SkeletonElementList()
        elements.append(catalogText("Conference AI Assistant"))
        elements.append(catalogText("Denne flaten kobler `ConferenceParticipantPreviewShell` og en eksplisitt `ConferenceAIGatewayPreview` sammen i ett ærlig arbeidsrom. Conference-state vises direkte ved siden av prompt, modelloppsett og siste AI-respons. Automatisk state-til-prompt-injeksjon er ikke aktiv ennå, så preset-knappene setter nyttige utkast som brukeren kan justere før invoke."))

        elements.append(
            catalogSection(
                "Conference Snapshot",
                content: [
                    catalogKeyText("conferenceParticipantShell.state.workspace.title"),
                    catalogKeyText("conferenceParticipantShell.state.workspace.subtitle"),
                    catalogKeyText("conferenceParticipantShell.state.workspace.participantBadge"),
                    catalogKeyText("conferenceParticipantShell.state.workspace.programBadge"),
                    catalogKeyText("conferenceParticipantShell.state.workspace.matchBadge"),
                    catalogKeyText("conferenceParticipantShell.state.workspace.meetingBadge"),
                    catalogKeyText("conferenceParticipantShell.state.workspace.nextStep"),
                    catalogKeyText("conferenceParticipantShell.state.workspace.previewNotice")
                ]
            )
        )

        elements.append(
            catalogSection(
                "Prompt-Ready Context",
                content: [
                    catalogText("Dette er de viktigste oppsummeringsfeltene fra participant-shellen akkurat nå. De er ment å være synlige side om side med agenten, slik at prompten kan finjusteres uten å måtte navigere bort."),
                    catalogKeyText("conferenceParticipantShell.state.program.agendaSummary"),
                    catalogKeyText("conferenceParticipantShell.state.program.timelineSummary"),
                    catalogKeyText("conferenceParticipantShell.state.matches.recommendationSummary"),
                    catalogKeyText("conferenceParticipantShell.state.matches.filterSummary"),
                    catalogKeyText("conferenceParticipantShell.state.meetings.meetingSummary"),
                    catalogKeyText("conferenceParticipantShell.state.meetings.requestSummary"),
                    catalogKeyText("conferenceParticipantShell.state.sharedConnections.connectionSummary"),
                    catalogKeyText("conferenceParticipantShell.state.sharedConnections.chatSummary")
                ]
            )
        )

        elements.append(
            catalogSection(
                "Copilot Setup",
                content: [
                    catalogKeyText("aiGateway.state.setup.statusLabel"),
                    catalogKeyText("aiGateway.state.setup.nextStep"),
                    catalogKeyText("aiGateway.state.setup.providerLabel"),
                    catalogKeyText("aiGateway.state.setup.credentialStatus"),
                    catalogKeyText("aiGateway.state.setup.storageHint"),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.applyDraftProfile",
                                label: "Hosted API",
                                payload: .object([
                                    "providerID": .string("openai-compatible"),
                                    "model": .string("gpt-4.1-mini"),
                                    "requiresAPIKey": .bool(true),
                                    "cachePolicy": .string("useCache")
                                ])
                            ),
                            catalogButton(
                                keypath: "aiGateway.applyDraftProfile",
                                label: "No-auth gateway",
                                payload: .object([
                                    "providerID": .string("openai-compatible"),
                                    "model": .string("gpt-4.1-mini"),
                                    "requiresAPIKey": .bool(false),
                                    "cachePolicy": .string("useCache")
                                ])
                            ),
                            catalogButton(keypath: "aiGateway.setDraftDeterministicMode", label: "Deterministic on", payload: .bool(true)),
                            catalogButton(keypath: "aiGateway.setDraftDeterministicMode", label: "Deterministic off", payload: .bool(false))
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Conference Prompt Presets",
                content: [
                    catalogText("Last inn et conference-spisset systemprompt først, og bruk deretter en task-preset eller skriv videre i promptfeltet."),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.setDraftSystemPrompt",
                                label: "Load copilot system prompt",
                                payload: .string(conferenceSystemPrompt)
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Daily brief",
                                payload: .string("Use the visible conference summaries in this workspace and give me a crisp brief for the rest of today: what matters most, what I should prepare for, and which session or conversation is highest leverage next.")
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Who should I meet?",
                                payload: .string("Based on the visible matchmaking, meeting, and shared-connection summaries, identify the three strongest people for me to meet next. Explain why each one matters and suggest a short opener for each conversation.")
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Follow-up plan",
                                payload: .string("Using the visible meeting and shared-connection summaries, draft a practical follow-up plan with owners, message drafts, and the next concrete step for each item.")
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Session priorities",
                                payload: .string("Use the agenda and program summaries in this workspace to rank the next sessions or activities for me. Explain the tradeoffs, what to skip, and what questions I should be ready to ask.")
                            )
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Prompt Draft",
                content: [
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.providerID",
                            targetKeypath: "aiGateway.setDraftProviderID",
                            placeholder: "Provider ID"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.model",
                            targetKeypath: "aiGateway.setDraftModel",
                            placeholder: "Model"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.baseURL",
                            targetKeypath: "aiGateway.setDraftBaseURL",
                            placeholder: "Optional base URL"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.apiKeyAlias",
                            targetKeypath: "aiGateway.setDraftAPIKeyAlias",
                            placeholder: "API key alias"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: nil,
                            targetKeypath: "aiGateway.setDraftAPIKey",
                            placeholder: "Paste API key and press Enter"
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.systemPrompt",
                            targetKeypath: "aiGateway.setDraftSystemPrompt",
                            placeholder: "Optional system prompt",
                            minLines: 4,
                            maxLines: 10,
                            submitOnEnter: false
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.prompt",
                            targetKeypath: "aiGateway.setDraftPrompt",
                            placeholder: "What should the conference copilot help with right now?",
                            minLines: 7,
                            maxLines: 18,
                            submitOnEnter: false
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(keypath: "aiGateway.invokeDraft", label: "Invoke conference copilot"),
                            catalogButton(keypath: "aiGateway.persistDraftAPIKey", label: "Save API key"),
                            catalogButton(keypath: "aiGateway.clearDraftAPIKey", label: "Clear session key")
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Latest AI Result",
                content: [
                    catalogKeyText("aiGateway.state.lastInvocation.outputPreview"),
                    catalogKeyText("aiGateway.state.lastInvocation.providerID"),
                    catalogKeyText("aiGateway.state.lastInvocation.model"),
                    catalogKeyText("aiGateway.state.lastInvocation.cacheHit"),
                    catalogKeyText("aiGateway.state.lastInvocation.invokeTimeMs"),
                    catalogKeyText("aiGateway.state.lastInvocation.quotaStatus"),
                    catalogKeyText("aiGateway.state.lastInvocation.warningsText"),
                    catalogKeyText("aiGateway.state.lastInvocation.errorsText"),
                    catalogKeyText("aiGateway.state.lastError")
                ]
            )
        )

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func configurationArchitectWorkspaceConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Cell Configuration Architect")
        configuration.description = "Arbeidsflate for aa finne eksisterende CellConfigurations eller utforme nye med katalogkontrakter, AI Agent Workspace og Cell Configuration Studio i samme skeleton."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConfigurationCatalog",
            sourceCellName: "ConfigurationCatalogCell",
            purpose: "CellConfiguration discovery og design",
            purposeDescription: "Bruk katalogkontrakter, AI Agent Workspace og Cell Configuration Studio side om side for aa finne eksisterende konfigurasjoner eller utforme komplette nye config-utkast.",
            interests: [
                "configuration",
                "catalog",
                "discovery",
                "ai",
                "copilot",
                "skeleton",
                "library",
                "binding",
                "web",
                "dashboard",
                "workspace",
                "personal",
                "purposeRef=purpose://capability.construct-cellconfiguration"
            ],
            menuSlots: ["upperLeft", "upperMid"]
        )

        var catalogReference = CellReference(endpoint: "cell:///ConfigurationCatalog", subscribeFeed: false, label: "configurationCatalog")
        catalogReference.setKeysAndValues = [
            KeyValue(key: "state", value: nil),
            KeyValue(key: "catalogContracts", value: nil),
            KeyValue(key: "configurations", value: nil)
        ]
        configuration.addReference(catalogReference)

        var studioReference = CellReference(endpoint: "cell:///CellConfigurationStudio", subscribeFeed: false, label: "configurationStudio")
        studioReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(studioReference)

        var aiReference = CellReference(endpoint: "cell:///AIGateway", subscribeFeed: false, label: "aiGateway")
        aiReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(aiReference)

        let architectSystemPrompt = AIGatewayConfigurationFactory.cellConfigurationArchitectSystemPrompt

        var elements = SkeletonElementList()
        elements.append(catalogText("Cell Configuration Architect"))
        elements.append(catalogText("Dette er hovedflaten for aa opprette, finne eller endre CellConfiguration/skeleton. Her finnes katalogkontraktene, Studio-state og AI-prompten som trengs for aa lage et trygt utkast uten aa gjette paa keypaths eller renderer-stoette."))

        elements.append(
            catalogSection(
                "Catalog Snapshot",
                content: [
                    catalogKeyText("configurationCatalog.state.count"),
                    catalogKeyText("configurationCatalog.state.purposes"),
                    catalogKeyText("configurationCatalog.state.upperLeftCount"),
                    catalogKeyText("configurationCatalog.state.upperMidCount"),
                    catalogKeyText("configurationCatalog.state.upperRightCount"),
                    catalogKeyText("configurationCatalog.state.lowerLeftCount"),
                    catalogKeyText("configurationCatalog.state.lowerMidCount"),
                    catalogKeyText("configurationCatalog.state.lowerRightCount")
                ]
            )
        )

        elements.append(
            catalogSection(
                "Studio State",
                content: [
                    catalogText("Studio-delen lar deg laste opp, versjonere og forhaandsvise en privat deltaker- eller adminflate. Det gir ikke rett til aa lese beskyttede admin-data eller publisere til en offisiell flate; begge deler krever separate Agreements autorisert av de respektive eiercellene."),
                    catalogKeyText("configurationStudio.state.workspace.title"),
                    catalogKeyText("configurationStudio.state.workspace.subtitle"),
                    catalogKeyText("configurationStudio.state.workspace.status"),
                    catalogKeyText("configurationStudio.state.selectionSummary"),
                    catalogKeyText("configurationStudio.state.draftSummary"),
                    catalogKeyText("configurationStudio.state.dirtySummary"),
                    catalogKeyText("configurationStudio.state.committedRevision"),
                    CellConfigurationStudioConfigurationFactory.privateDraftUpload(),
                    CellConfigurationStudioConfigurationFactory.privateDraftPreviewList(),
                    catalogButton(keypath: "configurationStudio.saveDraftVersion", label: "Save private version"),
                    catalogKeyText("configurationStudio.state.versionHistory.count"),
                    catalogKeyText("configurationStudio.state.versionHistory.activeVersionID"),
                    CellConfigurationStudioConfigurationFactory.privateVersionHistoryList()
                ]
            )
        )

        elements.append(
            catalogSection(
                "Architect Prompt Presets",
                content: [
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.setDraftSystemPrompt",
                                label: "Load architect prompt",
                                payload: .string(architectSystemPrompt)
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Find best existing config",
                                payload: .string("Use the visible catalog contracts to identify the best existing CellConfiguration for a user goal. Rank the top 3 visible candidates, explain why each one fits, and say what evidence from the contracts supports the ranking.")
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Draft new config",
                                payload: .string("Using only the visible catalog contracts and studio state, draft a complete CellConfiguration plan for a new user goal that is not already well covered. Include purpose, purposeDescription, interests, references, keypaths, skeleton sections, and validation steps.")
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Audit metadata coverage",
                                payload: .string("Review the visible catalog contracts and assess whether the descriptions are sufficient for reliable AI-based matching and generation. Call out weak or ambiguous purpose descriptions, thin interest coverage, and any places where the contract lacks enough detail to build a complete configuration safely.")
                            ),
                            catalogButton(
                                keypath: "configurationCatalog.syncScaffoldPurposeGoals",
                                label: "Sync catalog contracts",
                                payload: .object([:])
                            )
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "AI Setup",
                content: [
                    catalogKeyText("aiGateway.state.setup.statusLabel"),
                    catalogKeyText("aiGateway.state.setup.nextStep"),
                    catalogKeyText("aiGateway.state.setup.providerLabel"),
                    catalogKeyText("aiGateway.state.setup.credentialStatus"),
                    catalogKeyText("aiGateway.state.setup.storageHint"),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.applyDraftProfile",
                                label: "Hosted API",
                                payload: .object([
                                    "providerID": .string("openai-compatible"),
                                    "model": .string("gpt-4.1-mini"),
                                    "requiresAPIKey": .bool(true),
                                    "cachePolicy": .string("useCache")
                                ])
                            ),
                            catalogButton(
                                keypath: "aiGateway.applyDraftProfile",
                                label: "No-auth gateway",
                                payload: .object([
                                    "providerID": .string("openai-compatible"),
                                    "model": .string("gpt-4.1-mini"),
                                    "requiresAPIKey": .bool(false),
                                    "cachePolicy": .string("useCache")
                                ])
                            ),
                            catalogButton(keypath: "aiGateway.setDraftDeterministicMode", label: "Deterministic on", payload: .bool(true))
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Prompt Draft",
                content: [
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.providerID",
                            targetKeypath: "aiGateway.setDraftProviderID",
                            placeholder: "Provider ID"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.model",
                            targetKeypath: "aiGateway.setDraftModel",
                            placeholder: "Model"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.apiKeyAlias",
                            targetKeypath: "aiGateway.setDraftAPIKeyAlias",
                            placeholder: "API key alias"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: nil,
                            targetKeypath: "aiGateway.setDraftAPIKey",
                            placeholder: "Paste API key and press Enter"
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.systemPrompt",
                            targetKeypath: "aiGateway.setDraftSystemPrompt",
                            placeholder: "Architect system prompt",
                            minLines: 6,
                            maxLines: 14,
                            submitOnEnter: false
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.prompt",
                            targetKeypath: "aiGateway.setDraftPrompt",
                            placeholder: "What configuration should we find, evaluate, or design?",
                            minLines: 8,
                            maxLines: 20,
                            submitOnEnter: false
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(keypath: "aiGateway.invokeDraft", label: "Invoke architect"),
                            catalogButton(keypath: "aiGateway.persistDraftAPIKey", label: "Save API key"),
                            catalogButton(keypath: "aiGateway.clearDraftAPIKey", label: "Clear session key")
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Latest AI Result",
                content: [
                    catalogKeyText("aiGateway.state.lastInvocation.outputPreview"),
                    catalogKeyText("aiGateway.state.lastInvocation.providerID"),
                    catalogKeyText("aiGateway.state.lastInvocation.model"),
                    catalogKeyText("aiGateway.state.lastInvocation.cacheHit"),
                    catalogKeyText("aiGateway.state.lastInvocation.invokeTimeMs"),
                    catalogKeyText("aiGateway.state.lastInvocation.quotaStatus"),
                    catalogKeyText("aiGateway.state.lastInvocation.warningsText"),
                    catalogKeyText("aiGateway.state.lastInvocation.errorsText"),
                    catalogKeyText("aiGateway.state.lastError")
                ]
            )
        )

        var catalogContractsScrollModifiers = SkeletonModifiers()
        catalogContractsScrollModifiers.height = 360
        catalogContractsScrollModifiers.padding = 8
        catalogContractsScrollModifiers.background = "#07111A"
        catalogContractsScrollModifiers.cornerRadius = 8
        catalogContractsScrollModifiers.borderWidth = 1
        catalogContractsScrollModifiers.borderColor = "#1F3442"

        var catalogContractsScroll = SkeletonScrollView(
            axis: "vertical",
            elements: [
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "configurationCatalog.catalogContracts",
                        flowElementSkeleton: SkeletonVStack(elements: [
                            catalogKeyText("displayName"),
                            catalogKeyText("purpose"),
                            catalogKeyText("purposeDescription"),
                            catalogKeyText("tags"),
                            catalogKeyText("supportedTargetKinds"),
                            catalogKeyText("sourceCellEndpoint"),
                            .Divider(SkeletonDivider())
                        ])
                    )
                )
            ]
        )
        catalogContractsScroll.modifiers = catalogContractsScrollModifiers

        elements.append(
            catalogSection(
                "Catalog Contracts Reference",
                content: [
                    catalogText("Dette er referansematerialet arkitekten skal bruke naar den vurderer om en eksisterende CellConfiguration passer, eller hva et nytt utkast maa koble seg til."),
                    .ScrollView(catalogContractsScroll)
                ]
            )
        )

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func palazzoConciergeCopilotConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: RestaurantPalazzoAIProfile.configurationName)
        configuration.description = "Palazzo-orientert conciergeflate som kombinerer publisert vertskapskontekst, gjestesignal, visit intent, experience plan og embedded AIGateway i samme arbeidsflate."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///RestaurantExperiencePlan",
            sourceCellName: "RestaurantExperiencePlanCell",
            purpose: RestaurantPalazzoAIProfile.purpose,
            purposeDescription: "Bruk Palazzo sitt publiserte vertskapsinnhold, samtykkebasert gjestekontekst og embedded AIGateway for aa lage staff-usable opplevelsesplaner uten salgspress.",
            interests: ["restaurant", "hospitality", "concierge", "palazzo", "guest-experience", "ai", "copilot", "oslo"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var publishedContentReference = CellReference(endpoint: "cell:///RestaurantPublishedContent", subscribeFeed: false, label: "restaurantPublishedContent")
        publishedContentReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(publishedContentReference)

        var onboardingReference = CellReference(endpoint: "cell:///RestaurantOnboarding", subscribeFeed: false, label: "restaurantOnboarding")
        onboardingReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(onboardingReference)

        var visitContextReference = CellReference(endpoint: "cell:///RestaurantVisitContext", subscribeFeed: false, label: "restaurantVisitContext")
        visitContextReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(visitContextReference)

        var experiencePlanReference = CellReference(endpoint: "cell:///RestaurantExperiencePlan", subscribeFeed: false, label: "restaurantExperiencePlan")
        experiencePlanReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(experiencePlanReference)

        var knowledgeReference = CellReference(endpoint: "cell:///ConciergeKnowledgeCorpus", subscribeFeed: true, label: "conciergeKnowledge")
        knowledgeReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(knowledgeReference)

        var aiReference = CellReference(endpoint: "cell:///AIGateway", label: "aiGateway")
        aiReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(aiReference)

        var elements = SkeletonElementList()
        elements.append(catalogText(RestaurantPalazzoAIProfile.configurationName))
        elements.append(catalogText("Denne flaten viser hvor AI faktisk brukes i Palazzo-slicen. `RestaurantExperiencePlan.generatePlan` kan kalle `AIGatewayCell` med Palazzo-profilen, mens den embedded AIGateway-seksjonen lar deg laste samme profil manuelt og inspisere setup, prompt og siste respons."))

        elements.append(
            catalogSection(
                "Palazzo Snapshot",
                content: [
                    catalogKeyText("restaurantPublishedContent.state.landing.title"),
                    catalogKeyText("restaurantPublishedContent.state.landing.subtitle"),
                    catalogKeyText("restaurantPublishedContent.state.venue.name"),
                    catalogKeyText("restaurantPublishedContent.state.venue.neighborhood"),
                    catalogKeyText("restaurantPublishedContent.state.contentSummary"),
                    catalogKeyText("restaurantPublishedContent.state.lastPublishedAt")
                ]
            )
        )

        elements.append(
            catalogSection(
                "Guest Context",
                content: [
                    catalogText("Dette er den samtykkebaserte gjestekonteksten experience planneren faktisk leser i MVP-slicen."),
                    catalogKeyText("restaurantOnboarding.state.profileSummary"),
                    catalogKeyText("restaurantOnboarding.state.storageSummary"),
                    catalogKeyText("restaurantOnboarding.state.guest.displayName"),
                    catalogKeyText("restaurantOnboarding.state.guest.locale"),
                    catalogKeyText("restaurantOnboarding.state.current.capturedAt"),
                    catalogKeyText("restaurantOnboarding.state.eventCount")
                ]
            )
        )

        elements.append(
            catalogSection(
                "Visit Context",
                content: [
                    catalogKeyText("restaurantVisitContext.state.guestSummary"),
                    catalogKeyText("restaurantVisitContext.state.visitSummary"),
                    catalogKeyText("restaurantVisitContext.state.storageSummary"),
                    catalogKeyText("restaurantVisitContext.state.visit.occasion"),
                    catalogKeyText("restaurantVisitContext.state.visit.partySize"),
                    catalogKeyText("restaurantVisitContext.state.visit.timeWindowSummary"),
                    catalogKeyText("restaurantVisitContext.state.visit.externalBookingReference"),
                    catalogKeyText("restaurantVisitContext.state.visit.culturalContext"),
                    catalogKeyText("restaurantVisitContext.state.visit.status")
                ]
            )
        )

        elements.append(
            catalogSection(
                "Concierge Knowledge",
                content: [
                    catalogText("Kunnskapsbanken er gjesteklar for publisert meny, priser, allergenkoder og booking-handoff fra verifiserte kilder. Vinflasker, strenge allergier og reservasjonsendringer håndteres fortsatt med staff/booking-handoff."),
                    catalogKeyText("conciergeKnowledge.state.contractVersion"),
                    catalogKeyText("conciergeKnowledge.state.sourceCount"),
                    catalogKeyText("conciergeKnowledge.state.menuItemCount"),
                    catalogKeyText("conciergeKnowledge.state.guardrailSummary"),
                    catalogKeyText("conciergeKnowledge.state.lastActionSummary")
                ]
            )
        )

        elements.append(
            catalogSection(
                "Planning Actions",
                content: [
                    catalogKeyText("restaurantExperiencePlan.state.inputSummary"),
                    catalogKeyText("restaurantExperiencePlan.state.palazzoAIProfile.providerID"),
                    catalogKeyText("restaurantExperiencePlan.state.palazzoAIProfile.model"),
                    catalogKeyText("restaurantExperiencePlan.state.palazzoAIProfile.apiKeyAlias"),
                    catalogKeyText("restaurantExperiencePlan.state.palazzoAIProfile.credentialHint"),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "restaurantExperiencePlan.generatePlan",
                                label: "Heuristic plan",
                                payload: .object([
                                    "useAI": .bool(false)
                                ])
                            ),
                            catalogButton(
                                keypath: "restaurantExperiencePlan.generatePlan",
                                label: "Generate with Palazzo AI",
                                payload: RestaurantPalazzoAIProfile.generationPayload()
                            ),
                            catalogButton(
                                keypath: "restaurantExperiencePlan.approvePlan",
                                label: "Approve suggested plan",
                                payload: .object([:])
                            ),
                            catalogButton(keypath: "restaurantExperiencePlan.publishStaffBrief", label: "Publish staff brief")
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "AIGateway Setup",
                content: [
                    catalogKeyText("aiGateway.state.setup.statusLabel"),
                    catalogKeyText("aiGateway.state.setup.nextStep"),
                    catalogKeyText("aiGateway.state.setup.providerLabel"),
                    catalogKeyText("aiGateway.state.setup.credentialStatus"),
                    catalogKeyText("aiGateway.state.setup.storageHint"),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.applyDraftProfile",
                                label: "Load Palazzo AI profile",
                                payload: RestaurantPalazzoAIProfile.aiGatewayDraftProfilePayload()
                            ),
                            catalogButton(keypath: "aiGateway.setDraftDeterministicMode", label: "Deterministic on", payload: .bool(true)),
                            catalogButton(keypath: "aiGateway.setDraftRequiresAPIKey", label: "API key on", payload: .bool(true))
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Direct Prompt Draft",
                content: [
                    catalogText("Bruk denne delen hvis du vil inspisere eller teste Palazzo-profilen direkte i `AIGatewayCell`, uavhengig av restaurantcellens automatiske plan-call."),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.setDraftSystemPrompt",
                                label: "Load Palazzo system prompt",
                                payload: .string(RestaurantPalazzoAIProfile.systemPrompt)
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Hospitality review",
                                payload: .string(RestaurantPalazzoAIProfile.directPrompt)
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Tighten staff brief",
                                payload: .string("Use the visible guest context, visit context, and latest suggested plan in this workspace. Rewrite the staff brief so it is warmer, shorter, and easier for floor staff to act on without sounding sales-driven.")
                            )
                        ])
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.providerID",
                            targetKeypath: "aiGateway.setDraftProviderID",
                            placeholder: "Provider ID"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.model",
                            targetKeypath: "aiGateway.setDraftModel",
                            placeholder: "Model"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.apiKeyAlias",
                            targetKeypath: "aiGateway.setDraftAPIKeyAlias",
                            placeholder: "API key alias"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: nil,
                            targetKeypath: "aiGateway.setDraftAPIKey",
                            placeholder: "Paste API key and press Enter"
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.systemPrompt",
                            targetKeypath: "aiGateway.setDraftSystemPrompt",
                            placeholder: "Optional system prompt",
                            minLines: 4,
                            maxLines: 10,
                            submitOnEnter: false
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.prompt",
                            targetKeypath: "aiGateway.setDraftPrompt",
                            placeholder: "What should the Palazzo copilot help with right now?",
                            minLines: 7,
                            maxLines: 18,
                            submitOnEnter: false
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(keypath: "aiGateway.invokeDraft", label: "Invoke Palazzo copilot"),
                            catalogButton(keypath: "aiGateway.persistDraftAPIKey", label: "Save API key"),
                            catalogButton(keypath: "aiGateway.clearDraftAPIKey", label: "Clear session key")
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Plan And Staff Brief",
                content: [
                    catalogKeyText("restaurantExperiencePlan.state.aiStatus"),
                    catalogKeyText("restaurantExperiencePlan.state.aiMessage"),
                    catalogKeyText("restaurantExperiencePlan.state.suggestedPlan.aiProviderID"),
                    catalogKeyText("restaurantExperiencePlan.state.suggestedPlan.aiModel"),
                    catalogKeyText("restaurantExperiencePlan.state.staffBrief.title"),
                    catalogKeyText("restaurantExperiencePlan.state.staffBrief.subtitle"),
                    catalogKeyText("restaurantExperiencePlan.state.staffBrief.detail"),
                    catalogKeyText("restaurantExperiencePlan.state.staffBrief.note"),
                    catalogKeyText("restaurantExperiencePlan.state.eventCount"),
                    catalogKeyText("restaurantExperiencePlan.state.lastEventKind")
                ]
            )
        )

        elements.append(
            catalogSection(
                "Latest AI Result",
                content: [
                    catalogKeyText("aiGateway.state.lastInvocation.outputPreview"),
                    catalogKeyText("aiGateway.state.lastInvocation.providerID"),
                    catalogKeyText("aiGateway.state.lastInvocation.model"),
                    catalogKeyText("aiGateway.state.lastInvocation.cacheHit"),
                    catalogKeyText("aiGateway.state.lastInvocation.invokeTimeMs"),
                    catalogKeyText("aiGateway.state.lastInvocation.quotaStatus"),
                    catalogKeyText("aiGateway.state.lastInvocation.warningsText"),
                    catalogKeyText("aiGateway.state.lastInvocation.errorsText"),
                    catalogKeyText("aiGateway.state.lastError")
                ]
            )
        )

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func adminCopilotWorkspaceConfiguration(
        adminRouting: AdminControlPlaneRouting = .current
    ) -> CellConfiguration {
        AdminWorkspaceConfigurationFactory.copilotConfiguration(adminRouting: adminRouting)
    }

    static func adminControlPlaneOverviewConfiguration(
        adminRouting: AdminControlPlaneRouting = .current
    ) -> CellConfiguration {
        AdminWorkspaceConfigurationFactory.overviewConfiguration(adminRouting: adminRouting)
    }

    static func adminOperationsWorkspaceConfiguration(
        adminRouting: AdminControlPlaneRouting = .current
    ) -> CellConfiguration {
        AdminWorkspaceConfigurationFactory.operationsConfiguration(adminRouting: adminRouting)
    }

    static func adminSecurityWorkspaceConfiguration(
        adminRouting: AdminControlPlaneRouting = .current
    ) -> CellConfiguration {
        AdminWorkspaceConfigurationFactory.securityConfiguration(adminRouting: adminRouting)
    }

    static func adminProductAdministrationConfiguration(
        adminRouting: AdminControlPlaneRouting = .current
    ) -> CellConfiguration {
        AdminWorkspaceConfigurationFactory.productAdministrationConfiguration(adminRouting: adminRouting)
    }

    static func vaultStudioWorkspaceConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Vault Studio")
        configuration.description = "CellProtocol-native knowledge workspace rundt VaultCell snapshots, GraphStoreCell projeksjoner, AIGateway advisory output og MermaidRendererCell previews."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///VaultStudio",
            sourceCellName: "VaultStudioWorkspaceCell",
            purpose: "CellProtocol-native knowledge workspace",
            purposeDescription: "Skisser ideer, prosjekter og innhold med eksplisitte kontrakter, state snapshot, live sync via Flow og Mermaid-basert grafpreview.",
            interests: ["vault", "studio", "knowledge-graph", "markdown", "ai", "cellprotocol", "mermaid", "collaboration"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var vaultStudioReference = CellReference(endpoint: "cell:///VaultStudio", label: "vaultStudio")
        vaultStudioReference.setKeysAndValues = [KeyValue(key: "vaultStudio.refresh", value: .object([:]))]
        configuration.addReference(vaultStudioReference)

        var vaultReference = CellReference(endpoint: "cell:///Vault", label: "vault")
        vaultReference.setKeysAndValues = [KeyValue(key: "vault.state", value: nil)]
        configuration.addReference(vaultReference)

        var graphReference = CellReference(endpoint: "cell:///GraphStore", label: "graph")
        graphReference.setKeysAndValues = [
            KeyValue(key: "graph.state", value: nil),
            KeyValue(key: "graph.explorer.state", value: nil)
        ]
        configuration.addReference(graphReference)

        var aiReference = CellReference(endpoint: "cell:///AIGateway", label: "aiGateway")
        aiReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(aiReference)

        var mermaidReference = CellReference(endpoint: "cell:///MermaidRenderer", label: "mermaidRenderer")
        mermaidReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(mermaidReference)

        let navColumn = SkeletonElement.VStack(
            SkeletonVStack(
                elements: [
                    catalogText("Vault Studio"),
                    catalogKeyText("vaultStudio.state.syncPolicy.snapshotKeypath"),
                    .TextField(SkeletonTextField(placeholder: "Search · jump · invoke")),
                    catalogSection(
                        "Capture",
                        content: [
                            catalogKeyText("vaultStudio.state.navCounts.inbox"),
                            catalogKeyText("vaultStudio.state.navCounts.daily"),
                            catalogButton(
                                keypath: "vaultStudio.quickCapture",
                                label: "+ Quick capture",
                                payload: .object([
                                    "title": .string("Untitled capture"),
                                    "content": .string(""),
                                    "tags": .list([.string("inbox")])
                                ])
                            )
                        ]
                    ),
                    catalogSection(
                        "Workspace",
                        content: [
                            catalogKeyText("vaultStudio.state.navCounts.projects"),
                            catalogKeyText("vaultStudio.state.navCounts.drafts"),
                            catalogKeyText("vaultStudio.state.navCounts.references"),
                            .List(SkeletonList(keypath: "vaultStudio.state.notes"))
                        ]
                    ),
                    catalogSection(
                        "Explore",
                        content: [
                            catalogButton(
                                keypath: "vaultStudio.graphPreview",
                                label: "Render graph preview",
                                payload: .object(["depth": .integer(1)])
                            ),
                            catalogKeyText("graph.state.operations")
                        ]
                    )
                ],
                spacing: 10
            )
        )

        let editorColumn = SkeletonElement.ScrollView(
            SkeletonScrollView(
                axis: "vertical",
                elements: [
                    .HStack(
                        SkeletonHStack(
                            elements: [
                                catalogKeyText("vaultStudio.state.activeNoteID"),
                                catalogText("vault.note.get"),
                                catalogKeyText("vaultStudio.state.lastVaultStateVersion")
                            ],
                            spacing: 12
                        )
                    ),
                    .HStack(
                        SkeletonHStack(
                            elements: [
                                catalogButton(keypath: "vaultStudio.setMode", label: "Edit", payload: .string("edit")),
                                catalogButton(keypath: "vaultStudio.setMode", label: "Preview", payload: .string("preview")),
                                catalogButton(keypath: "vaultStudio.setMode", label: "Sketch", payload: .string("sketch")),
                                catalogButton(keypath: "vaultStudio.setMode", label: "Draft", payload: .string("draft"))
                            ],
                            spacing: 8
                        )
                    ),
                    catalogSection(
                        "Note",
                        content: [
                            catalogKeyText("vaultStudio.state.activeNote.id"),
                            catalogKeyText("vaultStudio.state.activeNote.tags"),
                            .TextField(
                                SkeletonTextField(
                                    sourceKeypath: "vaultStudio.state.activeNote.title",
                                    targetKeypath: "vaultStudio.setActiveTitle",
                                    placeholder: "Untitled"
                                )
                            ),
                            .TextArea(
                                SkeletonTextArea(
                                    sourceKeypath: "vaultStudio.state.activeNote.content",
                                    targetKeypath: "vaultStudio.setActiveContent",
                                    placeholder: "Start writing...",
                                    minLines: 18,
                                    maxLines: 36,
                                    editorMode: .richMarkdown
                                )
                            )
                        ]
                    ),
                    catalogSection(
                        "Status",
                        content: [
                            catalogKeyText("vaultStudio.state.mode"),
                            catalogKeyText("vaultStudio.state.syncPolicy.flowTopic"),
                            catalogKeyText("vaultStudio.state.syncPolicy.gapRule")
                        ]
                    )
                ]
            )
        )

        let rightPanelTabs = SkeletonElement.Tabs(
            SkeletonTabs(
                tabsKeypath: "vaultStudio.state.tabs",
                activeTabStateKeypath: "vaultStudio.state.panelTab",
                selectionActionKeypath: "vaultStudio.setPanelTab",
                idKeypath: "id",
                labelKeypath: "title",
                panels: [
                    SkeletonTabPanel(
                        id: "links",
                        content: [
                            catalogSection(
                                "GraphStoreCell.neighbors",
                                content: [
                                    catalogRenderedHTML("vaultStudio.state.graphPreview.rendered_html"),
                                    catalogKeyText("vaultStudio.state.graphPreview.source")
                                ]
                            ),
                            catalogSection(
                                "Backlinks · vault.links.backlinks",
                                content: [.List(SkeletonList(keypath: "vaultStudio.state.backlinks"))]
                            ),
                            catalogSection(
                                "Forward links · vault.links.forward",
                                content: [.List(SkeletonList(keypath: "vaultStudio.state.forwardLinks"))]
                            )
                        ]
                    ),
                    SkeletonTabPanel(
                        id: "ai",
                        content: [
                            catalogSection(
                                "AIGateway",
                                content: [
                                    catalogKeyText("aiGateway.state.setup.statusLabel"),
                                    .TextArea(
                                        SkeletonTextArea(
                                            sourceKeypath: "aiGateway.state.draft.prompt",
                                            targetKeypath: "aiGateway.setDraftPrompt",
                                            placeholder: "Ask for structure, critique, tasks or link ideas...",
                                            minLines: 5,
                                            maxLines: 10
                                        )
                                    ),
                                    catalogButton(keypath: "aiGateway.invokeDraft", label: "Invoke advisory AI"),
                                    catalogKeyText("vaultStudio.state.lastAIResult"),
                                    catalogKeyText("aiGateway.state.lastInvocation.outputPreview"),
                                    catalogText("Advisory only; AI output is not written to Vault unless a user action calls a Vault contract.")
                                ]
                            )
                        ]
                    ),
                    SkeletonTabPanel(
                        id: "collab",
                        content: [
                            catalogSection(
                                "Collab",
                                content: [
                                    catalogText("requires implementation work · capability.grant / capability.list"),
                                    .List(SkeletonList(keypath: "vaultStudio.state.implementationWork"))
                                ]
                            )
                        ]
                    ),
                    SkeletonTabPanel(
                        id: "audit",
                        content: [
                            catalogSection(
                                "Live Activity",
                                content: [
                                    catalogKeyText("vaultStudio.state.lastVaultStateVersion"),
                                    catalogKeyText("vaultStudio.state.lastRefreshEpochMs"),
                                    catalogText("Durable replay, revert and diff require later audit contracts.")
                                ]
                            )
                        ]
                    )
                ]
            )
        )

        let rightColumn = SkeletonElement.VStack(
            SkeletonVStack(
                elements: [rightPanelTabs],
                spacing: 10
            )
        )

        configuration.skeleton = .HStack(
            SkeletonHStack(
                elements: [navColumn, editorColumn, rightColumn],
                spacing: 16
            )
        )
        return configuration
    }

    static func vaultWorkspaceConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Vault Workspace (Obsidian-style)")
        configuration.description = "Vault/Obsidian workspace som eksponerer create, update, get, list og link-operasjoner via cell:///Vault-kontrakten."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///Vault",
            sourceCellName: "VaultCell",
            purpose: "Notatgraf (Obsidian-stil)",
            purposeDescription: "Opprett/list notater og koblinger via vault.note.* / vault.link.add for Obsidian-lignende arbeidsflyt.",
            interests: ["vault", "notes", "obsidian", "knowledge-graph", "markdown"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var reference = CellReference(endpoint: "cell:///Vault", label: "vault")
        reference.setKeysAndValues = [KeyValue(key: "vault.note.list", value: .object(vaultListNotesPayload(tags: ["obsidian"], limit: 20)))]
        configuration.addReference(reference)

        var elements = SkeletonElementList()
        elements.append(catalogText("Vault Workspace (Obsidian-style)"))
        elements.append(catalogText("Skeletonen speiler Vault MVP-kontrakten i web-laget. Full state-/resultatvisning krever at runtime faktisk registrerer cell:///Vault som celle, ikke bare API-bridge."))
        elements.append(contentsOf: vaultWorkspaceSections(
            referenceLabel: "vault",
            primaryNoteID: defaultVaultPrimaryNoteID,
            linkedNoteID: defaultVaultLinkedNoteID,
            listPayload: vaultListNotesPayload(tags: ["obsidian"], limit: 20),
            createPrimaryPayload: vaultCreateNotePayload(
                id: defaultVaultPrimaryNoteID,
                title: "Obsidian sample note",
                content: defaultVaultPrimaryContent,
                tags: ["obsidian", "mermaid", "staging"]
            ),
            createLinkedPayload: vaultCreateNotePayload(
                id: defaultVaultLinkedNoteID,
                title: "Obsidian linked note",
                content: "Linked from sample note.",
                tags: ["obsidian"]
            ),
            updatePrimaryPayload: vaultUpdateNotePayload(
                id: defaultVaultPrimaryNoteID,
                title: "Obsidian sample note (updated)",
                content: "# Mermaid + Vault\n\nUpdated from the skeleton action.\n",
                tags: ["obsidian", "mermaid", "updated"]
            ),
            getPrimaryPayload: vaultGetNotePayload(id: defaultVaultPrimaryNoteID),
            linkPayload: vaultAddLinkPayload(fromNoteID: defaultVaultPrimaryNoteID, toNoteID: defaultVaultLinkedNoteID)
        ))

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func obsidianAIWorkspaceConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Obsidian AI Workspace")
        configuration.description = "Obsidian-lignende knowledge workspace som kombinerer Vault noteoperasjoner med embedded AIGateway for sammendrag, strukturering og neste steg."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///Vault",
            sourceCellName: "VaultCell",
            purpose: "Obsidian copilot",
            purposeDescription: "Bruk Vault-notater og embedded AIGateway i samme arbeidsflate for å lese, oppdatere og videreutvikle kunnskapsnotater med lav friksjon.",
            interests: ["vault", "obsidian", "ai", "copilot", "notes", "markdown", "knowledge-graph", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var vaultReference = CellReference(endpoint: "cell:///Vault", label: "vault")
        vaultReference.setKeysAndValues = [KeyValue(key: "vault.note.list", value: .object(vaultListNotesPayload(tags: ["obsidian", "ai"], limit: 20)))]
        configuration.addReference(vaultReference)

        var aiReference = CellReference(endpoint: "cell:///AIGateway", label: "aiGateway")
        aiReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(aiReference)

        let noteCopilotSystemPrompt = """
        You are an Obsidian knowledge copilot. Help turn rough notes into useful structure, summaries, next actions, and cleaner links between ideas. Stay concrete and preserve the user's original meaning.
        """

        var elements = SkeletonElementList()
        elements.append(catalogText("Obsidian AI Workspace"))
        elements.append(catalogText("Denne flaten kombinerer den faktiske `Vault`-kontrakten med embedded `AIGateway`. Bruk Vault-seksjonene for å hente, opprette og oppdatere notater, og bruk AI-delen til å oppsummere, restrukturere eller foreslå neste steg. Automatisk note-til-prompt-injeksjon er ikke aktiv ennå, så arbeidsflyten er ærlig: notatdata og AI-draft vises side om side."))

        elements.append(contentsOf: vaultWorkspaceSections(
            referenceLabel: "vault",
            primaryNoteID: obsidianAIVaultPrimaryNoteID,
            linkedNoteID: obsidianAIVaultLinkedNoteID,
            listPayload: vaultListNotesPayload(tags: ["obsidian", "ai"], limit: 20),
            createPrimaryPayload: vaultCreateNotePayload(
                id: obsidianAIVaultPrimaryNoteID,
                title: "Obsidian AI sample note",
                content: obsidianAIVaultPrimaryContent,
                tags: ["obsidian", "ai", "copilot"]
            ),
            createLinkedPayload: vaultCreateNotePayload(
                id: obsidianAIVaultLinkedNoteID,
                title: "Obsidian AI linked note",
                content: "Linked note for follow-up ideas.",
                tags: ["obsidian", "ai"]
            ),
            updatePrimaryPayload: vaultUpdateNotePayload(
                id: obsidianAIVaultPrimaryNoteID,
                title: "Obsidian AI sample note (updated)",
                content: "# Obsidian AI Workspace\n\nUpdated from the combined Vault + AI workspace.\n",
                tags: ["obsidian", "ai", "updated"]
            ),
            getPrimaryPayload: vaultGetNotePayload(id: obsidianAIVaultPrimaryNoteID),
            linkPayload: vaultAddLinkPayload(fromNoteID: obsidianAIVaultPrimaryNoteID, toNoteID: obsidianAIVaultLinkedNoteID)
        ))

        elements.append(
            catalogSection(
                "AI Setup",
                content: [
                    catalogKeyText("aiGateway.state.setup.statusLabel"),
                    catalogKeyText("aiGateway.state.setup.nextStep"),
                    catalogKeyText("aiGateway.state.setup.providerLabel"),
                    catalogKeyText("aiGateway.state.setup.credentialStatus"),
                    catalogKeyText("aiGateway.state.setup.storageHint"),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.applyDraftProfile",
                                label: "Hosted API",
                                payload: .object([
                                    "providerID": .string("openai-compatible"),
                                    "model": .string("gpt-4.1-mini"),
                                    "requiresAPIKey": .bool(true),
                                    "cachePolicy": .string("useCache")
                                ])
                            ),
                            catalogButton(
                                keypath: "aiGateway.applyDraftProfile",
                                label: "No-auth gateway",
                                payload: .object([
                                    "providerID": .string("openai-compatible"),
                                    "model": .string("gpt-4.1-mini"),
                                    "requiresAPIKey": .bool(false),
                                    "cachePolicy": .string("useCache")
                                ])
                            ),
                            catalogButton(keypath: "aiGateway.setDraftDeterministicMode", label: "Deterministic on", payload: .bool(true))
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Note Prompt Presets",
                content: [
                    catalogText("Last inn et note-spisset systemprompt, og bruk deretter preset-knappene som utgangspunkt for den konkrete notatjobben du vil gjøre."),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.setDraftSystemPrompt",
                                label: "Load note copilot system prompt",
                                payload: .string(noteCopilotSystemPrompt)
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Summarize note",
                                payload: .string("Summarize the active note into a compact overview with the main idea, open questions, and what is still unclear.")
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Turn into outline",
                                payload: .string("Turn the active note into a cleaner outline with headings, bullet points, and a short next-step section.")
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Suggest backlinks",
                                payload: .string("Suggest likely backlinks, tags, and linked-note ideas based on the active note. Explain why each link would help the knowledge graph.")
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Action list",
                                payload: .string("Convert the active note into a practical action list with priorities, unknowns, and the smallest next useful step.")
                            )
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "AI Draft",
                content: [
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.providerID",
                            targetKeypath: "aiGateway.setDraftProviderID",
                            placeholder: "Provider ID"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.model",
                            targetKeypath: "aiGateway.setDraftModel",
                            placeholder: "Model"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.apiKeyAlias",
                            targetKeypath: "aiGateway.setDraftAPIKeyAlias",
                            placeholder: "API key alias"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: nil,
                            targetKeypath: "aiGateway.setDraftAPIKey",
                            placeholder: "Paste API key and press Enter"
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.systemPrompt",
                            targetKeypath: "aiGateway.setDraftSystemPrompt",
                            placeholder: "Optional system prompt",
                            minLines: 4,
                            maxLines: 10,
                            submitOnEnter: false
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.prompt",
                            targetKeypath: "aiGateway.setDraftPrompt",
                            placeholder: "What should the Obsidian copilot help with right now?",
                            minLines: 7,
                            maxLines: 18,
                            submitOnEnter: false
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(keypath: "aiGateway.invokeDraft", label: "Invoke Obsidian copilot"),
                            catalogButton(keypath: "aiGateway.persistDraftAPIKey", label: "Save API key"),
                            catalogButton(keypath: "aiGateway.clearDraftAPIKey", label: "Clear session key")
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Latest AI Result",
                content: [
                    catalogKeyText("aiGateway.state.lastInvocation.outputPreview"),
                    catalogKeyText("aiGateway.state.lastInvocation.providerID"),
                    catalogKeyText("aiGateway.state.lastInvocation.model"),
                    catalogKeyText("aiGateway.state.lastInvocation.cacheHit"),
                    catalogKeyText("aiGateway.state.lastInvocation.invokeTimeMs"),
                    catalogKeyText("aiGateway.state.lastInvocation.warningsText"),
                    catalogKeyText("aiGateway.state.lastInvocation.errorsText"),
                    catalogKeyText("aiGateway.state.lastError")
                ]
            )
        )

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func todoPlannerCopilotConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Todo Planner Copilot")
        configuration.description = "Planleggingsflate som kombinerer personlige todo-lister med embedded AIGateway for prioritering, ukesplan og neste steg."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///Todo",
            sourceCellName: "TodoCell",
            purpose: "Todo planner copilot",
            purposeDescription: "Bruk den faktiske Todo-kontrakten side om side med embedded AIGateway for daglig planlegging, prioritering og ukesreview.",
            interests: ["todo", "planning", "ai", "copilot", "priority", "weekly-review", "personal-productivity", "web"],
            menuSlots: ["lowerMid", "lowerRight"]
        )

        var todoReference = CellReference(endpoint: "cell:///Todo", label: "todo")
        todoReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(todoReference)

        var aiReference = CellReference(endpoint: "cell:///AIGateway", label: "aiGateway")
        aiReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(aiReference)

        let plannerSystemPrompt = """
        You are a pragmatic planning copilot. Use the visible task state from this workspace, keep recommendations concrete, and prefer the smallest next step that reduces user friction. Separate observation, prioritization, and suggested actions.
        """

        var elements = SkeletonElementList()
        elements.append(catalogText("Todo Planner Copilot"))
        elements.append(catalogText("Denne flaten kombinerer den faktiske `Todo`-cellen med embedded `AIGateway`. Bruk todo-delen til å legge til og rydde oppgaver, og bruk AI-delen til å lage en plan, finne fokus for dagen eller skrive et kort ukesreview basert på synlig state."))

        elements.append(
            catalogSection(
                "Planning Snapshot",
                content: [
                    catalogKeyText("todo.state.summaryText"),
                    catalogText("Direkte task-handlinger bruker fremdeles `todo.addTodo`, `todo.toggleTodo`, `todo.setTodoDue`, `todo.setTodoPriority`, `todo.setTodoLabels`, `todo.setTodoImportant`, `todo.setTodoRecurrence`, `todo.clearCompleted` og de øvrige keypaths fra Todo-cellen.")
                ]
            )
        )

        elements.append(
            catalogSection(
                "Quick Capture",
                content: [
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "todo.addTodo",
                                label: "Quick add",
                                payload: .object([
                                    "title": .string("Ny oppgave"),
                                    "priority": .integer(2)
                                ])
                            ),
                            catalogButton(
                                keypath: "todo.addTodo",
                                label: "Add for today",
                                payload: .object([
                                    "title": .string("Oppgave for i dag"),
                                    "dueAt": .string("today"),
                                    "important": .bool(true)
                                ])
                            ),
                            catalogButton(
                                keypath: "todo.addTodo",
                                label: "Weekly review",
                                payload: .object([
                                    "title": .string("Ukentlig review"),
                                    "dueAt": .string("today"),
                                    "recurrence": .string("weekly"),
                                    "labels": .list([.string("review")])
                                ])
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "todo.queryTodos",
                                label: "Query important",
                                payload: .object([
                                    "status": .string("active"),
                                    "bucket": .string("important"),
                                    "sortBy": .string("priority"),
                                    "order": .string("asc"),
                                    "limit": .integer(10)
                                ])
                            ),
                            catalogButton(keypath: "todo.clearCompleted", label: "Clear completed", payload: .bool(true))
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Today",
                content: [
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "todo.state.todayItems",
                            flowElementSkeleton: todoPlannerItemRowSkeleton()
                        )
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Important",
                content: [
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "todo.state.importantItems",
                            flowElementSkeleton: todoPlannerItemRowSkeleton()
                        )
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Overdue",
                content: [
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "todo.state.overdueItems",
                            flowElementSkeleton: todoPlannerItemRowSkeleton()
                        )
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Inbox",
                content: [
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "todo.state.activeItems",
                            flowElementSkeleton: todoPlannerItemRowSkeleton()
                        )
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Completed",
                content: [
                    .List(
                        SkeletonList(
                            topic: nil,
                            keypath: "todo.state.completedItems",
                            flowElementSkeleton: todoPlannerItemRowSkeleton()
                        )
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "AI Setup",
                content: [
                    catalogKeyText("aiGateway.state.setup.statusLabel"),
                    catalogKeyText("aiGateway.state.setup.nextStep"),
                    catalogKeyText("aiGateway.state.setup.providerLabel"),
                    catalogKeyText("aiGateway.state.setup.credentialStatus"),
                    catalogKeyText("aiGateway.state.setup.storageHint"),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.applyDraftProfile",
                                label: "Hosted API",
                                payload: .object([
                                    "providerID": .string("openai-compatible"),
                                    "model": .string("gpt-4.1-mini"),
                                    "requiresAPIKey": .bool(true),
                                    "cachePolicy": .string("useCache")
                                ])
                            ),
                            catalogButton(
                                keypath: "aiGateway.applyDraftProfile",
                                label: "No-auth gateway",
                                payload: .object([
                                    "providerID": .string("openai-compatible"),
                                    "model": .string("gpt-4.1-mini"),
                                    "requiresAPIKey": .bool(false),
                                    "cachePolicy": .string("useCache")
                                ])
                            ),
                            catalogButton(keypath: "aiGateway.setDraftDeterministicMode", label: "Deterministic on", payload: .bool(true))
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Planner Prompt Presets",
                content: [
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.setDraftSystemPrompt",
                                label: "Use planner system prompt",
                                payload: .string(plannerSystemPrompt)
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Plan my day",
                                payload: .string("Using the visible todo state, create a realistic plan for today. Rank the tasks by leverage, identify what can wait, and suggest the smallest concrete next step for each high-priority item.")
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Prioritize backlog",
                                payload: .string("Review the visible inbox, overdue, and important tasks. Group them into do now, schedule later, delegate, or drop, and explain the reasoning briefly.")
                            ),
                            catalogButton(
                                keypath: "aiGateway.setDraftPrompt",
                                label: "Weekly review",
                                payload: .string("Use the visible todo lists to draft a short weekly review. Summarize progress, unfinished commitments, recurring obligations, and the 3 most important focus areas for next week.")
                            )
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Prompt Draft",
                content: [
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.providerID",
                            targetKeypath: "aiGateway.setDraftProviderID",
                            placeholder: "Provider ID"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.model",
                            targetKeypath: "aiGateway.setDraftModel",
                            placeholder: "Model"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.baseURL",
                            targetKeypath: "aiGateway.setDraftBaseURL",
                            placeholder: "Optional base URL"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.apiKeyAlias",
                            targetKeypath: "aiGateway.setDraftAPIKeyAlias",
                            placeholder: "API key alias"
                        )
                    ),
                    .TextField(
                        SkeletonTextField(
                            text: nil,
                            sourceKeypath: nil,
                            targetKeypath: "aiGateway.setDraftAPIKey",
                            placeholder: "Paste API key and press Enter"
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.systemPrompt",
                            targetKeypath: "aiGateway.setDraftSystemPrompt",
                            placeholder: "Optional system prompt",
                            minLines: 4,
                            maxLines: 10,
                            submitOnEnter: false
                        )
                    ),
                    .TextArea(
                        SkeletonTextArea(
                            text: nil,
                            sourceKeypath: "aiGateway.state.draft.prompt",
                            targetKeypath: "aiGateway.setDraftPrompt",
                            placeholder: "What should the planner copilot help with right now?",
                            minLines: 7,
                            maxLines: 18,
                            submitOnEnter: false
                        )
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(keypath: "aiGateway.invokeDraft", label: "Invoke planner copilot"),
                            catalogButton(keypath: "aiGateway.persistDraftAPIKey", label: "Save API key"),
                            catalogButton(keypath: "aiGateway.clearDraftAPIKey", label: "Clear session key")
                        ])
                    )
                ]
            )
        )

        elements.append(
            catalogSection(
                "Latest AI Result",
                content: [
                    catalogKeyText("aiGateway.state.lastInvocation.outputPreview"),
                    catalogKeyText("aiGateway.state.lastInvocation.providerID"),
                    catalogKeyText("aiGateway.state.lastInvocation.model"),
                    catalogKeyText("aiGateway.state.lastInvocation.cacheHit"),
                    catalogKeyText("aiGateway.state.lastInvocation.invokeTimeMs"),
                    catalogKeyText("aiGateway.state.lastInvocation.quotaStatus"),
                    catalogKeyText("aiGateway.state.lastInvocation.warningsText"),
                    catalogKeyText("aiGateway.state.lastInvocation.errorsText"),
                    catalogKeyText("aiGateway.state.lastError")
                ]
            )
        )

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    static func ideaTaskShareConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Idea Task Share")
        configuration.description = "Read-only delt snapshot av en valgt ide og relaterte todoer. Brukes som launchflate for invite-handoff via Participation Hub, ikke som delt live-state over personlig Vault/Todo."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///IdeaTaskShare",
            sourceCellName: "IdeaTaskShareCell",
            purpose: "Delt idesnapshot",
            purposeDescription: "Mottakeren leser state foerst, abonnerer deretter paa share-feed og kan resynce ved behov.",
            interests: ["ideas", "todo", "sharing", "snapshot", "review", "cellprotocol"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var shareReference = CellReference(endpoint: "cell:///IdeaTaskShare", label: "ideaTaskShare")
        shareReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(shareReference)

        configuration.skeleton = .VStack(
            SkeletonVStack(
                elements: [
                    catalogText("Idea Task Share"),
                    catalogKeyText("ideaTaskShare.state.summary"),
                    catalogKeyText("ideaTaskShare.state.purpose"),
                    catalogKeyText("ideaTaskShare.state.subscriptionHint"),
                    catalogSection(
                        "Shared Idea",
                        content: [
                            catalogKeyText("ideaTaskShare.state.selectedIdea.title"),
                            catalogKeyText("ideaTaskShare.state.selectedIdea.stageLabel"),
                            catalogKeyText("ideaTaskShare.state.selectedIdea.tagsText"),
                            catalogKeyText("ideaTaskShare.state.selectedIdea.contentPreview"),
                            catalogKeyText("ideaTaskShare.state.collaborationStatus")
                        ]
                    ),
                    catalogSection(
                        "Related Tasks",
                        content: [
                            catalogKeyText("ideaTaskShare.state.relatedTodoCount"),
                            .List(
                                SkeletonList(
                                    topic: nil,
                                    keypath: "ideaTaskShare.state.relatedTodos",
                                    flowElementSkeleton: ideaTaskTodoRowSkeleton()
                                )
                            )
                        ]
                    ),
                    catalogSection(
                        "Metadata",
                        content: [
                            catalogKeyText("ideaTaskShare.state.ownerDisplayName"),
                            catalogKeyText("ideaTaskShare.state.ownerEntityRef"),
                            catalogKeyText("ideaTaskShare.state.shareEndpoint"),
                            catalogKeyText("ideaTaskShare.state.publishedAtEpochMs"),
                            catalogKeyText("ideaTaskShare.state.updatedAtEpochMs"),
                            catalogKeyText("ideaTaskShare.state.updateCount"),
                            catalogKeyText("ideaTaskShare.state.syncPolicy.feedTopic"),
                            catalogKeyText("ideaTaskShare.state.syncPolicy.refreshHint")
                        ]
                    )
                ]
            )
        )
        return configuration
    }

    static func ideaTaskWorkspaceConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Idea Task Workspace")
        configuration.description = "Personlig idé-til-handling-workspace som gjør løs idé om til ett konkret neste steg, med Vault som idé-lager og Todo som oppgavelager."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///IdeaTaskWorkspace",
            sourceCellName: "IdeaTaskWorkspaceCell",
            purpose: "Idé til handling",
            purposeDescription: "Fang en idé, forstå hva som bør skje nå, og gjør den om til en konkret Todo eller et minste neste steg. Invite-ready snapshotdeling finnes, men delt live backlog på personlige Vault/Todo-celler påstås ikke.",
            interests: ["ideas", "todo", "vault", "planning", "next-step", "personal-productivity", "cellprotocol"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var workspaceReference = CellReference(endpoint: "cell:///IdeaTaskWorkspace", label: "ideaWorkspace")
        workspaceReference.setKeysAndValues = [
            KeyValue(key: "refresh", value: .object([:])),
            KeyValue(key: "state", value: nil)
        ]
        configuration.addReference(workspaceReference)

        var vaultStudioReference = CellReference(endpoint: "cell:///VaultStudio", label: "vaultStudio")
        vaultStudioReference.setKeysAndValues = [
            KeyValue(key: "refresh", value: .object([:])),
            KeyValue(key: "state", value: nil)
        ]
        configuration.addReference(vaultStudioReference)

        var todoReference = CellReference(endpoint: "cell:///Todo", label: "todo")
        todoReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(todoReference)

        var participationHubReference = CellReference(endpoint: "cell:///ParticipationHub", label: "participationHub")
        participationHubReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(participationHubReference)

        var aiGatewayReference = CellReference(endpoint: "cell:///AIGateway", label: "aiGateway")
        aiGatewayReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(aiGatewayReference)

        let captureCard = catalogCardSection(
            "Capture",
            content: [
                dashboardKeyText("ideaWorkspace.state.emptyState.detail", fontSize: 13),
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "ideaWorkspace.state.captureDraft.title",
                        targetKeypath: "ideaWorkspace.setCaptureTitle",
                        placeholder: "Kort idetittel"
                    )
                ),
                .TextArea(
                    SkeletonTextArea(
                        sourceKeypath: "ideaWorkspace.state.captureDraft.content",
                        targetKeypath: "ideaWorkspace.setCaptureContent",
                        placeholder: "Skriv rått. Hva er ideen, hvorfor betyr den noe, hva kan være første lille steg?",
                        minLines: 5,
                        maxLines: 10,
                        submitOnEnter: false,
                        editorMode: .richMarkdown
                    )
                ),
                ideaTaskActionButton(keypath: "ideaWorkspace.captureIdea", label: "Fang idé", emphasis: true)
            ]
        )

        let nextStepCard = catalogCardSection(
            "Neste handling",
            content: [
                dashboardKeyText("ideaWorkspace.state.nextStep.title", fontSize: 22, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("ideaWorkspace.state.nextStep.detail", fontSize: 14),
                dashboardKeyText("ideaWorkspace.state.nextStep.reason", fontSize: 12, foregroundColor: "#9AC4CF"),
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "ideaWorkspace.state.nextStepDraft.title",
                        targetKeypath: "ideaWorkspace.setNextStepDraftTitle",
                        placeholder: "Juster foreslått oppgave eller steg"
                    )
                ),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            .TextField(
                                SkeletonTextField(
                                    sourceKeypath: "ideaWorkspace.state.nextStepDraft.due",
                                    targetKeypath: "ideaWorkspace.setNextStepDraftDue",
                                    placeholder: "Frist, f.eks. today"
                                )
                            ),
                            .TextField(
                                SkeletonTextField(
                                    sourceKeypath: "ideaWorkspace.state.nextStepDraft.priorityText",
                                    targetKeypath: "ideaWorkspace.setNextStepDraftPriority",
                                    placeholder: "P1-P4"
                                )
                            )
                        ],
                        spacing: 8
                    )
                ),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            ideaTaskActionButton(keypath: "ideaWorkspace.acceptNextStep", label: "Gjør dette nå", emphasis: true),
                            ideaTaskActionButton(keypath: "ideaWorkspace.analyzeSelectedIdea", label: "Foreslå bedre")
                        ],
                        spacing: 8
                    )
                ),
                dashboardStaticText("AI-forslag er rådgivende. Ingenting lagres før du velger hovedhandlingen.", fontSize: 12, foregroundColor: "#9AC4CF"),
                dashboardKeyText("ideaWorkspace.state.aiSuggestion.advisoryText", fontSize: 12, foregroundColor: "#C8E7D2")
            ]
        )

        let selectedIdeaCard = catalogCardSection(
            "Valgt idé",
            content: [
                dashboardKeyText("ideaWorkspace.state.selectedIdea.title", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("ideaWorkspace.state.selectedIdea.stageLabel", fontSize: 12, foregroundColor: "#7FD6D0"),
                dashboardKeyText("ideaWorkspace.state.selectedIdea.contentPreview", fontSize: 13),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            ideaTaskActionButton(keypath: "ideaWorkspace.setIdeaStage", label: "Inbox", payload: .string("inbox")),
                            ideaTaskActionButton(keypath: "ideaWorkspace.setIdeaStage", label: "Project", payload: .string("project")),
                            ideaTaskActionButton(keypath: "ideaWorkspace.setIdeaStage", label: "Review", payload: .string("review"))
                        ],
                        spacing: 8
                    )
                )
            ]
        )

        let editorCard = catalogCardSection(
            "Notat",
            content: [
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "vaultStudio.state.activeNote.title",
                        targetKeypath: "vaultStudio.setActiveTitle",
                        placeholder: "Untitled idea"
                    )
                ),
                .TextArea(
                    SkeletonTextArea(
                        sourceKeypath: "vaultStudio.state.activeNote.content",
                        targetKeypath: "vaultStudio.setActiveContent",
                        placeholder: "Videreutvikle den valgte ideen...",
                        minLines: 14,
                        maxLines: 28,
                        submitOnEnter: false,
                        editorMode: .richMarkdown
                    )
                )
            ]
        )

        let taskCard = catalogCardSection(
            "Relaterte oppgaver",
            content: [
                dashboardKeyText("ideaWorkspace.state.relatedTodoCount", fontSize: 12, foregroundColor: "#9AC4CF"),
                dashboardKeyText("ideaWorkspace.state.selectedTodo.title", fontSize: 16, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("ideaWorkspace.state.selectedTodo.stepProgressText", fontSize: 12),
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "ideaWorkspace.state.stepDraft.title",
                        targetKeypath: "ideaWorkspace.setStepDraftTitle",
                        placeholder: "Nytt delsteg for valgt oppgave"
                    )
                ),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            ideaTaskActionButton(keypath: "ideaWorkspace.promoteIdeaToTodo", label: "Lag Todo", emphasis: true),
                            ideaTaskActionButton(keypath: "ideaWorkspace.addStepToSelectedTodo", label: "Legg til steg")
                        ],
                        spacing: 8
                    )
                ),
                selectableDashboardList(
                    keypath: "ideaWorkspace.state.relatedTodos",
                    selectionStateKeypath: "ideaWorkspace.state.selectedTodoID",
                    selectionActionKeypath: "ideaWorkspace.selectTodo",
                    rowSkeleton: ideaTaskTodoRowSkeleton()
                )
            ]
        )

        let focusPanel = SkeletonTabPanel(
            id: "focus",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 430)],
                        spacing: 12,
                        elements: [captureCard, nextStepCard, selectedIdeaCard, taskCard, editorCard]
                    )
                )
            ]
        )

        let inboxPanel = SkeletonTabPanel(
            id: "inbox",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 280, max: 420)],
                        spacing: 12,
                        elements: [
                            captureCard,
                            catalogCardSection(
                                "Inbox",
                                content: [
                                    selectableDashboardList(
                                        keypath: "ideaWorkspace.state.inboxIdeas",
                                        selectionStateKeypath: "ideaWorkspace.state.selectedIdeaID",
                                        selectionActionKeypath: "ideaWorkspace.selectIdea",
                                        rowSkeleton: ideaTaskIdeaRowSkeleton()
                                    )
                                ]
                            ),
                            catalogCardSection(
                                "Project",
                                content: [
                                    selectableDashboardList(
                                        keypath: "ideaWorkspace.state.projectIdeas",
                                        selectionStateKeypath: "ideaWorkspace.state.selectedIdeaID",
                                        selectionActionKeypath: "ideaWorkspace.selectIdea",
                                        rowSkeleton: ideaTaskIdeaRowSkeleton()
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )

        let mapPanel = SkeletonTabPanel(
            id: "map",
            content: [
                catalogCardSection(
                    "Idé-kart",
                    content: [
                        dashboardKeyText("ideaWorkspace.state.ideaGraph.summaryText", fontSize: 13, foregroundColor: "#9AC4CF"),
                        .Visualization(
                            SkeletonVisualization(
                                kind: "network",
                                keypath: "ideaWorkspace.state.ideaGraph",
                                stateKeypath: "ideaWorkspace.state.ideaGraph",
                                actionKeypath: "ideaWorkspace.selectIdea"
                            )
                        )
                    ]
                ),
                catalogCardSection(
                    "Fokus-kø",
                    content: [
                        selectableDashboardList(
                            keypath: "ideaWorkspace.state.focusQueue",
                            selectionStateKeypath: "ideaWorkspace.state.selectedIdeaID",
                            selectionActionKeypath: "ideaWorkspace.selectIdea",
                            rowSkeleton: ideaTaskIdeaRowSkeleton()
                        )
                    ]
                )
            ]
        )

        let reviewPanel = SkeletonTabPanel(
            id: "review",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 280, max: 420)],
                        spacing: 12,
                        elements: [
                            catalogCardSection(
                                "Review",
                                content: [
                                    selectableDashboardList(
                                        keypath: "ideaWorkspace.state.reviewIdeas",
                                        selectionStateKeypath: "ideaWorkspace.state.selectedIdeaID",
                                        selectionActionKeypath: "ideaWorkspace.selectIdea",
                                        rowSkeleton: ideaTaskIdeaRowSkeleton()
                                    )
                                ]
                            ),
                            selectedIdeaCard,
                            nextStepCard
                        ]
                    )
                )
            ]
        )

        let sharePanel = SkeletonTabPanel(
            id: "share",
            content: [
                catalogCardSection(
                    "Invite-ready snapshot",
                    content: [
                        dashboardKeyText("ideaWorkspace.state.collaboration.statusText", fontSize: 13),
                        dashboardKeyText("ideaWorkspace.state.collaboration.sharedIdeaTitle", fontSize: 16, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                        .TextField(
                            SkeletonTextField(
                                sourceKeypath: "ideaWorkspace.state.collaboration.inviteDraft.targetEntityRef",
                                targetKeypath: "ideaWorkspace.setInviteTargetEntityRef",
                                placeholder: "Mottaker entity-ref"
                            )
                        ),
                        .TextField(
                            SkeletonTextField(
                                sourceKeypath: "ideaWorkspace.state.collaboration.inviteDraft.targetHubEndpoint",
                                targetKeypath: "ideaWorkspace.setInviteTargetHubEndpoint",
                                placeholder: "Mottakers ParticipationHub-endepunkt"
                            )
                        ),
                        .HStack(
                            SkeletonHStack(
                                elements: [
                                    ideaTaskActionButton(keypath: "ideaWorkspace.prepareShareInvite", label: "Klargjør snapshot", emphasis: true),
                                    ideaTaskActionButton(keypath: "ideaWorkspace.deliverShareInvite", label: "Send invite")
                                ],
                                spacing: 8
                            )
                        ),
                        dashboardStaticText("Share er snapshot + feed. Dette åpner ikke personlig Vault/Todo som delt live backlog.", fontSize: 12, foregroundColor: "#9AC4CF")
                    ]
                )
            ]
        )

        configuration.skeleton = .VStack(
            SkeletonVStack(
                elements: [
                    catalogCardSection(
                        "Ideer til handling",
                        content: [
                            dashboardKeyText("ideaWorkspace.state.workspaceSubtitle", fontSize: 14),
                            dashboardKeyText("ideaWorkspace.state.productHealth.nextActionText", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                            dashboardKeyText("ideaWorkspace.state.productHealth.frictionBudget", fontSize: 12, foregroundColor: "#7FD6D0")
                        ]
                    ),
                    .Tabs(
                        SkeletonTabs(
                            tabsKeypath: "ideaWorkspace.state.tabs",
                            activeTabStateKeypath: "ideaWorkspace.state.activeTabID",
                            selectionActionKeypath: "ideaWorkspace.setActiveTab",
                            idKeypath: "id",
                            labelKeypath: "title",
                            panels: [focusPanel, inboxPanel, mapPanel, reviewPanel, sharePanel]
                        )
                    )
                ],
                spacing: 12
            )
        )
        return configuration
    }

    static func havenWorkbenchConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "HAVEN Workbench")
        configuration.description = "V0.5 prosjekt- og oppgaveflate som samler canonical work items, ideinntak, triage, backlog, portfolio, roadmap, graf, GitHub-sync og docs."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///WorkItem",
            sourceCellName: "WorkItemCell",
            purpose: "HAVEN project workbench",
            purposeDescription: "Fang ideer, features, bugs og utestaaende arbeid som canonical WorkItem records, triager dem mot portfolio/roadmap/GitHub/docs, og bruk board/kanban/Trello-lignende state-first Flow-events for sync.",
            interests: ["haven", "projects", "tasks", "bugs", "features", "triage", "roadmap", "portfolio", "graph", "github", "docs", "board", "kanban", "trello", "purposeRef=haven.work.board.view", "cellprotocol"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var workItemsReference = CellReference(endpoint: "cell:///WorkItem", label: "workItems")
        workItemsReference.setKeysAndValues = [
            KeyValue(key: "state", value: nil),
            KeyValue(key: "syncStatus", value: nil)
        ]
        configuration.addReference(workItemsReference)

        var projectPortfolioReference = CellReference(endpoint: "cell:///ProjectPortfolio", subscribeFeed: false, label: "projectPortfolio")
        projectPortfolioReference.setKeysAndValues = [
            KeyValue(key: "state", value: nil),
            KeyValue(key: "syncStatus", value: nil),
            KeyValue(key: "feed", value: nil)
        ]
        configuration.addReference(projectPortfolioReference)

        var ownerSetupReference = CellReference(endpoint: "cell:///WorkbenchOwnerSetup", label: "ownerSetup")
        ownerSetupReference.setKeysAndValues = [
            KeyValue(key: "state", value: nil),
            KeyValue(key: "contracts", value: nil)
        ]
        configuration.addReference(ownerSetupReference)

        var githubSyncReference = CellReference(endpoint: "cell:///GitHubWorkSync", label: "githubSync")
        githubSyncReference.setKeysAndValues = [
            KeyValue(key: "state", value: nil),
            KeyValue(key: "syncStatus", value: nil)
        ]
        configuration.addReference(githubSyncReference)

        var workspaceReference = CellReference(endpoint: "cell:///IdeaTaskWorkspace", label: "ideaWorkspace")
        workspaceReference.setKeysAndValues = [
            KeyValue(key: "refresh", value: .object([:])),
            KeyValue(key: "state", value: nil)
        ]
        configuration.addReference(workspaceReference)

        var vaultStudioReference = CellReference(endpoint: "cell:///VaultStudio", label: "vaultStudio")
        vaultStudioReference.setKeysAndValues = [
            KeyValue(key: "refresh", value: .object([:])),
            KeyValue(key: "state", value: nil)
        ]
        configuration.addReference(vaultStudioReference)

        var todoReference = CellReference(endpoint: "cell:///Todo", label: "todo")
        todoReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(todoReference)

        var serviceCatalogReference = CellReference(endpoint: "cell:///ServiceCatalog", label: "serviceCatalog")
        serviceCatalogReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(serviceCatalogReference)

        var draftVersionReference = CellReference(endpoint: "cell:///DraftVersion", label: "draftVersions")
        draftVersionReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(draftVersionReference)

        var graphReference = CellReference(endpoint: "cell:///GraphStore", label: "graph")
        graphReference.setKeysAndValues = [
            KeyValue(key: "graph.state", value: nil),
            KeyValue(key: "graph.explorer.state", value: nil)
        ]
        configuration.addReference(graphReference)

        var ragReference = CellReference(endpoint: "cell:///RAGGateway", label: "rag")
        ragReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(ragReference)

        var aiGatewayReference = CellReference(endpoint: "cell:///AIGateway", label: "aiGateway")
        aiGatewayReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(aiGatewayReference)

        let statusPanel = SkeletonTabPanel(
            id: "status",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 460)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchProjectStatusCard(),
                            workItemTrackerListCard("Aktivt naa", keypath: "workItems.state.inProgressItems"),
                            workItemTrackerListCard("Neste klare oppgaver", keypath: "workItems.state.readyItems"),
                            workItemTrackerListCard("Blokkert / risiko", keypath: "workItems.state.dependencyRiskItems"),
                            workItemTrackerListCard("Ferdig", keypath: "workItems.state.doneItems"),
                            havenWorkbenchProjectListCard("Aktive prosjekter", keypath: "projectPortfolio.state.activeProjects"),
                            havenWorkbenchProjectListCard("Kommende prosjekter", keypath: "projectPortfolio.state.upcomingProjects"),
                            havenWorkbenchProjectListCard("Ferdige prosjekter", keypath: "projectPortfolio.state.doneProjects"),
                            havenWorkbenchOwnerSetupCard()
                        ]
                    )
                )
            ]
        )

        let allWorkItemsPanel = SkeletonTabPanel(
            id: "all",
            content: [
                havenWorkbenchAllWorkItemsCard()
            ]
        )

        let inboxPanel = SkeletonTabPanel(
            id: "inbox",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 430)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchIntakeCard(),
                            havenWorkbenchSyncStatusCard(),
                            havenWorkbenchNextActionCard(),
                            havenWorkbenchEvidenceCard()
                        ]
                    )
                )
            ]
        )

        let triagePanel = SkeletonTabPanel(
            id: "triage",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 430)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchFocusQueueCard(),
                            havenWorkbenchSavedViewsCard(),
                            havenWorkbenchInboxCard(),
                            havenWorkbenchRiskCard(),
                            havenWorkbenchDependencyTableCard()
                        ]
                    )
                )
            ]
        )

        let backlogPanel = SkeletonTabPanel(
            id: "backlog",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 430)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchBacklogSummaryCard(),
                            havenWorkbenchRiskCard(),
                            havenWorkbenchTodayCard(),
                            havenWorkbenchPlannedCard(),
                            havenWorkbenchQuickActionsCard()
                        ]
                    )
                )
            ]
        )

        let boardPanel = SkeletonTabPanel(
            id: "board",
            content: [
                .VStack(
                    SkeletonVStack(
                        elements: [
                            havenWorkbenchBoardSurface(),
                            havenWorkbenchOwnerSetupCard()
                        ],
                        spacing: 12
                    )
                )
            ]
        )

        let projectsPanel = SkeletonTabPanel(
            id: "projects",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 460)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchProjectStatusCard(),
                            havenWorkbenchProjectIntakeCard(),
                            havenWorkbenchProjectListCard("Active projects", keypath: "projectPortfolio.state.activeProjects"),
                            havenWorkbenchProjectListCard("Risk projects", keypath: "projectPortfolio.state.riskProjects"),
                            havenWorkbenchServiceCatalogCard(),
                            havenWorkbenchImplementationQueueCard(),
                            havenWorkbenchDraftsCard(),
                            havenWorkbenchOwnerSetupCard()
                        ]
                    )
                )
            ]
        )

        let roadmapPanel = SkeletonTabPanel(
            id: "roadmap",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 320, max: 540)],
                        spacing: 12,
                        elements: [
                            projectPortfolioRoadmapTableCard(),
                            projectPortfolioMilestoneTimelineCard(),
                            projectPortfolioReleaseCard(),
                            projectPortfolioCapacityCard(),
                            havenWorkbenchProjectListCard("Upcoming projects", keypath: "projectPortfolio.state.upcomingProjects"),
                            havenWorkbenchProjectListCard("Overdue projects", keypath: "projectPortfolio.state.overdueProjects"),
                            havenWorkbenchProjectListCard("Stale projects", keypath: "projectPortfolio.state.staleProjects")
                        ]
                    )
                )
            ]
        )

        let graphPanel = SkeletonTabPanel(
            id: "graph",
            content: [
                .VStack(
                    SkeletonVStack(
                        elements: [
                            havenWorkbenchRelationMapCard(),
                            .Grid(
                                SkeletonGrid(
                                    columns: [.adaptive(min: 320, max: 520)],
                                    spacing: 12,
                                    elements: [
                                        havenWorkbenchDependencyGraphCard(),
                                        havenWorkbenchGraphStoreCard(),
                                        havenWorkbenchCoverageChartCard()
                                    ]
                                )
                            )
                        ],
                        spacing: 12
                    )
                )
            ]
        )

        let githubPanel = SkeletonTabPanel(
            id: "github",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 320, max: 540)],
                        spacing: 12,
                        elements: [
                            githubWorkSyncStatusCard(),
                            githubWorkSyncRepoCard(),
                            githubWorkSyncImportCard(),
                            githubWorkSyncOutboundCard()
                        ]
                    )
                )
            ]
        )

        let docsPanel = SkeletonTabPanel(
            id: "docs",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 460)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchDocsCard(),
                            havenWorkbenchAICard(),
                            havenWorkbenchKnownGapsCard()
                        ]
                    )
                )
            ]
        )

        configuration.skeleton = .VStack(
            SkeletonVStack(
                elements: [
                    catalogCardSection(
                        "HAVEN Workbench",
                        content: [
                            dashboardKeyText("workItems.state.summaryText", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                            dashboardKeyText("projectPortfolio.state.summaryText", fontSize: 14, fontWeight: "semibold", foregroundColor: "#8DE1DA"),
                            dashboardKeyText("ideaWorkspace.state.productHealth.nextActionText", fontSize: 13, foregroundColor: "#9AC4CF"),
                            dashboardKeyText("ownerSetup.state.requesterIdentityUUID", fontSize: 11, foregroundColor: "#8EA3AD"),
                            .HStack(
                                SkeletonHStack(
                                    elements: [
                                        dashboardBadgeKeyText("projectPortfolio.state.riskCount"),
                                        dashboardBadgeKeyText("workItems.state.blockedCount"),
                                        dashboardBadgeKeyText("workItems.state.implementationGapCount"),
                                        dashboardBadgeKeyText("projectPortfolio.state.releaseCount"),
                                        dashboardBadgeKeyText("githubSync.state.importedItemCount"),
                                        dashboardBadgeKeyText("githubSync.state.outboundQueueCount"),
                                        dashboardBadgeKeyText("todo.state.summaryText"),
                                        dashboardBadgeKeyText("serviceCatalog.state.implementationQueueCount"),
                                        dashboardBadgeKeyText("graph.graph.state.nodeCount"),
                                        catalogButton(
                                            keypath: "ownerSetup.seedOwnerWorkbench",
                                            label: "Sett opp min Workbench",
                                            payload: .object(["source": .string("haven-workbench-summary")])
                                        )
                                    ],
                                    spacing: 8
                                )
                            )
                        ]
                    ),
                    .Tabs(
                        SkeletonTabs(
                            activeTabStateKeypath: "",
                            panels: [statusPanel, allWorkItemsPanel, boardPanel, inboxPanel, triagePanel, backlogPanel, projectsPanel, roadmapPanel, graphPanel, githubPanel, docsPanel]
                        )
                    ),
                    havenWorkbenchSelectedWorkItemPanel()
                ],
                spacing: 12
            )
        )
        return configuration
    }

    static func workItemTrackerConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Work Item Tracker")
        configuration.description = "Standalone V0-flate for canonical HAVEN work items."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///WorkItem",
            sourceCellName: "WorkItemCell",
            purpose: "Canonical HAVEN work items",
            purposeDescription: "Fang og triager ideer, features, bugs, docs, research, beslutninger og implementation gaps med evidens, relasjoner og neste handling.",
            interests: ["haven", "work-items", "bugs", "features", "triage", "backlog", "implementation-gaps", "cellprotocol"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var workItemsReference = CellReference(endpoint: "cell:///WorkItem", label: "workItems")
        workItemsReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(workItemsReference)

        let intakePanel = SkeletonTabPanel(
            id: "intake",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 430)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchIntakeCard(),
                            workItemTrackerSummaryCard()
                        ]
                    )
                )
            ]
        )
        let boardPanel = SkeletonTabPanel(
            id: "board",
            content: [
                havenWorkbenchBoardSurface()
            ]
        )
        let allPanel = SkeletonTabPanel(
            id: "all",
            content: [
                havenWorkbenchAllWorkItemsCard()
            ]
        )
        let triagePanel = SkeletonTabPanel(
            id: "triage",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 430)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchFocusQueueCard(),
                            workItemTrackerListCard("Ready", keypath: "workItems.state.readyItems"),
                            havenWorkbenchRiskCard()
                        ]
                    )
                )
            ]
        )
        let activePanel = SkeletonTabPanel(
            id: "active",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 430)],
                        spacing: 12,
                        elements: [
                            workItemTrackerListCard("In progress", keypath: "workItems.state.inProgressItems"),
                            workItemTrackerListCard("Bugs", keypath: "workItems.state.bugs"),
                            workItemTrackerListCard("Implementation gaps", keypath: "workItems.state.implementationGaps")
                        ]
                    )
                )
            ]
        )
        let donePanel = SkeletonTabPanel(
            id: "done",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 430)],
                        spacing: 12,
                        elements: [
                            workItemTrackerListCard("Done / won't do", keypath: "workItems.state.doneItems"),
                            havenWorkbenchQuickActionsCard()
                        ]
                    )
                )
            ]
        )

        configuration.skeleton = .VStack(
            SkeletonVStack(
                elements: [
                    catalogCardSection(
                        "Work Item Tracker",
                        content: [
                            dashboardStaticText("Canonical V0 for arbeid som AI-assistenter og mennesker skal kunne finne igjen."),
                            dashboardKeyText("workItems.state.summaryText", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF")
                        ]
                    ),
                    .Tabs(
                        SkeletonTabs(
                            activeTabStateKeypath: "",
                            panels: [intakePanel, allPanel, boardPanel, triagePanel, activePanel, donePanel]
                        )
                    ),
                    havenWorkbenchSelectedWorkItemPanel()
                ],
                spacing: 12
            )
        )
        return configuration
    }

    static func projectPortfolioConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Project Portfolio")
        configuration.description = "Standalone V0-flate for canonical HAVEN projects."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ProjectPortfolio",
            sourceCellName: "ProjectPortfolioCell",
            purpose: "Canonical HAVEN project portfolio",
            purposeDescription: "Fang og vedlikehold prosjektstatus, helse, prioritet, planleggingsdatoer, milestones, releases, capacity, saved views, repo-/celleref og lenker til WorkItem. Roadmap har native read-only Gantt/timeline med tabellfallback.",
            interests: ["haven", "projects", "portfolio", "roadmap", "health", "planning", "work-items", "releases", "capacity", "saved-views"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var projectPortfolioReference = CellReference(endpoint: "cell:///ProjectPortfolio", subscribeFeed: false, label: "projectPortfolio")
        projectPortfolioReference.setKeysAndValues = [
            KeyValue(key: "state", value: nil),
            KeyValue(key: "feed", value: nil)
        ]
        configuration.addReference(projectPortfolioReference)

        let intakePanel = SkeletonTabPanel(
            id: "intake",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 430)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchProjectIntakeCard(),
                            havenWorkbenchProjectStatusCard()
                        ]
                    )
                )
            ]
        )
        let portfolioPanel = SkeletonTabPanel(
            id: "portfolio",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 460)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchProjectListCard("Top projects", keypath: "projectPortfolio.state.topProjects"),
                            havenWorkbenchProjectListCard("Active projects", keypath: "projectPortfolio.state.activeProjects"),
                            havenWorkbenchProjectListCard("Done / archived", keypath: "projectPortfolio.state.doneProjects")
                        ]
                    )
                )
            ]
        )
        let roadmapPanel = SkeletonTabPanel(
            id: "roadmap",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 320, max: 540)],
                        spacing: 12,
                        elements: [
                            projectPortfolioRoadmapTableCard(),
                            projectPortfolioMilestoneTimelineCard(),
                            projectPortfolioReleaseCard(),
                            havenWorkbenchProjectListCard("Upcoming projects", keypath: "projectPortfolio.state.upcomingProjects"),
                            havenWorkbenchProjectListCard("Overdue projects", keypath: "projectPortfolio.state.overdueProjects")
                        ]
                    )
                )
            ]
        )
        let riskPanel = SkeletonTabPanel(
            id: "risk",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 460)],
                        spacing: 12,
                        elements: [
                            havenWorkbenchProjectListCard("Risk projects", keypath: "projectPortfolio.state.riskProjects"),
                            havenWorkbenchProjectListCard("Blocked projects", keypath: "projectPortfolio.state.blockedProjects")
                        ]
                    )
                )
            ]
        )
        let activityPanel = SkeletonTabPanel(
            id: "activity",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 300, max: 460)],
                        spacing: 12,
                        elements: [
                            projectPortfolioActivityCard(),
                            havenWorkbenchProjectListCard("Recent projects", keypath: "projectPortfolio.state.recentProjects")
                        ]
                    )
                )
            ]
        )

        configuration.skeleton = .VStack(
            SkeletonVStack(
                elements: [
                    catalogCardSection(
                        "Project Portfolio",
                        content: [
                            dashboardStaticText("Canonical V0 for prosjektstatus, helse og lenker mellom repoer, celler og work items."),
                            dashboardKeyText("projectPortfolio.state.summaryText", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                            dashboardKeyText("projectPortfolio.state.selectedProject.name", fontSize: 14, foregroundColor: "#8DE1DA")
                        ]
                    ),
                    .Tabs(
                        SkeletonTabs(
                            activeTabStateKeypath: "",
                            panels: [intakePanel, portfolioPanel, roadmapPanel, riskPanel, activityPanel]
                        )
                    )
                ],
                spacing: 12
            )
        )
        return configuration
    }

    static func githubWorkSyncConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "GitHub Work Sync")
        configuration.description = "Standalone V0.5-flate for lokal GitHub issue/PR-import til WorkItem-payloads og eksplisitt outbound sync-ko."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///GitHubWorkSync",
            sourceCellName: "GitHubWorkSyncCell",
            purpose: "GitHub work sync",
            purposeDescription: "Konfigurer repo-mapping, importer offline issue/PR-fixtures til WorkItem payloads, se CI/check-status og ko ekstern write-back bare ved eksplisitt brukerhandling.",
            interests: ["haven", "github", "issues", "pull-requests", "work-items", "sync", "ci", "cellprotocol"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var githubReference = CellReference(endpoint: "cell:///GitHubWorkSync", label: "githubSync")
        githubReference.setKeysAndValues = [
            KeyValue(key: "state", value: nil),
            KeyValue(key: "syncStatus", value: nil),
            KeyValue(key: "contracts", value: nil)
        ]
        configuration.addReference(githubReference)

        var workItemsReference = CellReference(endpoint: "cell:///WorkItem", label: "workItems")
        workItemsReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(workItemsReference)

        let overviewPanel = SkeletonTabPanel(
            id: "overview",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 320, max: 540)],
                        spacing: 12,
                        elements: [githubWorkSyncStatusCard(), githubWorkSyncRepoCard()]
                    )
                )
            ]
        )
        let importPanel = SkeletonTabPanel(
            id: "imports",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 320, max: 540)],
                        spacing: 12,
                        elements: [githubWorkSyncImportCard(), havenWorkbenchFocusQueueCard()]
                    )
                )
            ]
        )
        let outboundPanel = SkeletonTabPanel(
            id: "outbound",
            content: [
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 320, max: 540)],
                        spacing: 12,
                        elements: [githubWorkSyncOutboundCard(), havenWorkbenchSyncStatusCard()]
                    )
                )
            ]
        )

        configuration.skeleton = .VStack(
            SkeletonVStack(
                elements: [
                    catalogCardSection(
                        "GitHub Work Sync",
                        content: [
                            dashboardStaticText("Lokal import/read-sync for issues og PRs. Ekstern write-back blir bare lagt i ko via eksplisitt handling."),
                            dashboardKeyText("githubSync.state.externalWriteMode", fontSize: 14, fontWeight: "semibold", foregroundColor: "#F6C66F"),
                            dashboardKeyText("githubSync.state.importedItemCount"),
                            dashboardKeyText("githubSync.state.outboundQueueCount")
                        ]
                    ),
                    .Tabs(
                        SkeletonTabs(
                            activeTabStateKeypath: "",
                            panels: [overviewPanel, importPanel, outboundPanel]
                        )
                    )
                ],
                spacing: 12
            )
        )
        return configuration
    }

    private static func workItemTrackerSummaryCard() -> SkeletonElement {
        catalogCardSection(
            "Status",
            content: [
                dashboardKeyText("workItems.state.totalCount"),
                dashboardKeyText("workItems.state.openCount"),
                dashboardKeyText("workItems.state.blockedCount"),
                dashboardKeyText("workItems.state.bugCount"),
                dashboardKeyText("workItems.state.featureCount"),
                dashboardKeyText("workItems.state.implementationGapCount")
            ]
        )
    }

    private static func workItemTrackerListCard(_ title: String, keypath: String) -> SkeletonElement {
        catalogCardSection(
            title,
            content: [
                selectableDashboardList(
                    keypath: keypath,
                    selectionStateKeypath: "workItems.state.selectedItemID",
                    selectionActionKeypath: "workItems.select",
                    rowSkeleton: havenWorkbenchWorkItemRowSkeleton()
                )
            ]
        )
    }

    private static func havenWorkbenchAllWorkItemsCard() -> SkeletonElement {
        catalogCardSection(
            "All work items",
            content: [
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "workItems.state.filterText",
                        targetKeypath: "workItems.setFilterText",
                        placeholder: "Search title, ID, project, label, status or priority"
                    )
                ),
                dashboardStaticText("Press Enter to apply or clear the search.", fontSize: 11, foregroundColor: "#9AC4CF"),
                dashboardKeyText("workItems.state.filteredCount", fontSize: 12, foregroundColor: "#9AC4CF"),
                selectableDashboardList(
                    keypath: "workItems.state.filteredItems",
                    selectionStateKeypath: "workItems.state.selectedItemID",
                    selectionActionKeypath: "workItems.select",
                    rowSkeleton: havenWorkbenchWorkItemRowSkeleton()
                )
            ]
        )
    }

    private static func havenWorkbenchOwnerSetupCard() -> SkeletonElement {
        catalogCardSection(
            "Min Workbench",
            content: [
                dashboardKeyText("ownerSetup.state.summaryText", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("ownerSetup.state.identityMode", fontSize: 12, foregroundColor: "#8DE1DA"),
                dashboardKeyText("ownerSetup.state.requesterIdentityUUID", fontSize: 11, foregroundColor: "#8EA3AD"),
                dashboardKeyText("ownerSetup.state.ownerRule", fontSize: 12, foregroundColor: "#D5E4ED"),
                dashboardKeyText("ownerSetup.state.sharingRule", fontSize: 12, foregroundColor: "#F6C66F"),
                catalogButton(
                    keypath: "ownerSetup.seedOwnerWorkbench",
                    label: "Sett opp min Workbench",
                    payload: .object(["source": .string("haven-workbench-owner-card")])
                ),
                dashboardKeyText("ownerSetup.state.lastResult.summaryText", fontSize: 12, foregroundColor: "#8DE1DA"),
                dashboardKeyText("ownerSetup.state.lastResult.nextStep", fontSize: 12, foregroundColor: "#9AC4CF")
            ]
        )
    }

    private static func havenWorkbenchIntakeCard() -> SkeletonElement {
        catalogCardSection(
            "Intake",
            content: [
                dashboardStaticText("Fang ideer, features, bugs, docs, research og utestaaende arbeid som canonical work items. Skillen beskriver hvordan assistenter skal fylle feltene."),
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "workItems.state.captureDraft.title",
                        targetKeypath: "workItems.setDraftTitle",
                        placeholder: "Tittel: bug, feature, ide eller utestaaende"
                    )
                ),
                .TextArea(
                    SkeletonTextArea(
                        sourceKeypath: "workItems.state.captureDraft.summary",
                        targetKeypath: "workItems.setDraftSummary",
                        placeholder: "Beskriv kontekst, forventet oppfoersel, faktisk oppfoersel, prosjekt/repo, evidens, forslag til neste steg.",
                        minLines: 6,
                        maxLines: 14,
                        submitOnEnter: false,
                        editorMode: .richMarkdown
                    )
                ),
                havenWorkbenchWorkItemKindPicker(),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            .TextField(
                                SkeletonTextField(
                                    sourceKeypath: "workItems.state.captureDraft.project",
                                    targetKeypath: "workItems.setDraftProject",
                                    placeholder: "Prosjekt"
                                )
                            ),
                            .TextField(
                                SkeletonTextField(
                                    sourceKeypath: "workItems.state.captureDraft.source",
                                    targetKeypath: "workItems.setDraftSource",
                                    placeholder: "Kilde"
                                )
                            )
                        ],
                        spacing: 8
                    )
                ),
                ideaTaskActionButton(keypath: "workItems.captureDraft", label: "Fang work item", emphasis: true)
            ]
        )
    }

    private static func havenWorkbenchNextActionCard() -> SkeletonElement {
        catalogCardSection(
            "Neste trygge steg",
            content: [
                dashboardKeyText("ideaWorkspace.state.nextStep.title", fontSize: 20, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("ideaWorkspace.state.nextStep.detail", fontSize: 13),
                dashboardKeyText("ideaWorkspace.state.nextStep.reason", fontSize: 12, foregroundColor: "#9AC4CF"),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            ideaTaskActionButton(keypath: "ideaWorkspace.acceptNextStep", label: "Aksepter neste steg", emphasis: true),
                            ideaTaskActionButton(keypath: "ideaWorkspace.analyzeSelectedIdea", label: "Foreslaa bedre")
                        ],
                        spacing: 8
                    )
                ),
                dashboardKeyText("ideaWorkspace.state.aiSuggestion.advisoryText", fontSize: 12, foregroundColor: "#C8E7D2")
            ]
        )
    }

    private static func havenWorkbenchEvidenceCard() -> SkeletonElement {
        catalogCardSection(
            "Evidens og notat",
            content: [
                dashboardKeyText("ideaWorkspace.state.selectedIdea.title", fontSize: 16, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("ideaWorkspace.state.selectedIdea.tagsText", fontSize: 12, foregroundColor: "#9AC4CF"),
                dashboardKeyText("ideaWorkspace.state.selectedIdea.contentPreview", fontSize: 13),
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "vaultStudio.state.activeNote.title",
                        targetKeypath: "vaultStudio.setActiveTitle",
                        placeholder: "Arbeidsnotat"
                    )
                ),
                .TextArea(
                    SkeletonTextArea(
                        sourceKeypath: "vaultStudio.state.activeNote.content",
                        targetKeypath: "vaultStudio.setActiveContent",
                        placeholder: "Legg til lenker, observasjoner, repro-steg, kilder eller beslutninger.",
                        minLines: 8,
                        maxLines: 20,
                        submitOnEnter: false,
                        editorMode: .richMarkdown
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchFocusQueueCard() -> SkeletonElement {
        catalogCardSection(
            "Triage-koe",
            content: [
                dashboardKeyText("workItems.state.summaryText", fontSize: 12, foregroundColor: "#9AC4CF"),
                selectableDashboardList(
                    keypath: "workItems.state.triageItems",
                    selectionStateKeypath: "workItems.state.selectedItemID",
                    selectionActionKeypath: "workItems.select",
                    rowSkeleton: havenWorkbenchWorkItemRowSkeleton()
                )
            ]
        )
    }

    private static func havenWorkbenchInboxCard() -> SkeletonElement {
        catalogCardSection(
            "Ideer i workspace",
            content: [
                selectableDashboardList(
                    keypath: "ideaWorkspace.state.inboxIdeas",
                    selectionStateKeypath: "ideaWorkspace.state.selectedIdeaID",
                    selectionActionKeypath: "ideaWorkspace.selectIdea",
                    rowSkeleton: ideaTaskIdeaRowSkeleton()
                )
            ]
        )
    }

    private static func havenWorkbenchRiskCard() -> SkeletonElement {
        catalogCardSection(
            "Risiko og blokkere",
            content: [
                dashboardKeyText("workItems.state.dependencyRiskCount", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("workItems.state.statusBlockedCount", fontSize: 12, foregroundColor: "#F6C66F"),
                dashboardKeyText("workItems.state.blockedByCount", fontSize: 12, foregroundColor: "#F6C66F"),
                dashboardKeyText("workItems.state.blockingCount", fontSize: 12, foregroundColor: "#8DE1DA"),
                dashboardStaticText("Dependency risk viser status=blocked, work items som er blokkert av andre, og work items som blokkerer annet arbeid."),
                selectableDashboardList(
                    keypath: "workItems.state.dependencyRiskItems",
                    selectionStateKeypath: "workItems.state.selectedItemID",
                    selectionActionKeypath: "workItems.select",
                    rowSkeleton: havenWorkbenchWorkItemRowSkeleton()
                )
            ]
        )
    }

    private static func havenWorkbenchDependencyTableCard() -> SkeletonElement {
        catalogCardSection(
            "Dependency risk table",
            content: [
                .Visualization(
                    SkeletonVisualization(
                        kind: "table",
                        keypath: "workItems.state.dependencyRiskTable",
                        stateKeypath: "workItems.state.selectedItemID"
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchDependencyGraphCard() -> SkeletonElement {
        catalogCardSection(
            "Work dependencies",
            content: [
                dashboardKeyText("workItems.state.relationshipCount", fontSize: 14, fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("workItems.state.dependencyCount", fontSize: 12, foregroundColor: "#F6C66F"),
                dashboardKeyText("workItems.state.blockingCount", fontSize: 12, foregroundColor: "#8DE1DA"),
                .Visualization(
                    SkeletonVisualization(
                        kind: "table",
                        keypath: "workItems.state.relationshipTable",
                        stateKeypath: "workItems.state.selectedItemID"
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchBacklogSummaryCard() -> SkeletonElement {
        catalogCardSection(
            "Backlog-status",
            content: [
                dashboardKeyText("workItems.state.summaryText", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("workItems.state.featureCount"),
                dashboardKeyText("workItems.state.bugCount"),
                dashboardKeyText("workItems.state.implementationGapCount"),
                dashboardKeyText("todo.state.summaryText", fontSize: 12, foregroundColor: "#9AC4CF")
            ]
        )
    }

    private static func havenWorkbenchTodayCard() -> SkeletonElement {
        catalogCardSection(
            "In progress",
            content: [
                selectableDashboardList(
                    keypath: "workItems.state.inProgressItems",
                    selectionStateKeypath: "workItems.state.selectedItemID",
                    selectionActionKeypath: "workItems.select",
                    rowSkeleton: havenWorkbenchWorkItemRowSkeleton()
                )
            ]
        )
    }

    private static func havenWorkbenchPlannedCard() -> SkeletonElement {
        catalogCardSection(
            "Ready / gaps",
            content: [
                selectableDashboardList(
                    keypath: "workItems.state.readyItems",
                    selectionStateKeypath: "workItems.state.selectedItemID",
                    selectionActionKeypath: "workItems.select",
                    rowSkeleton: havenWorkbenchWorkItemRowSkeleton()
                ),
                selectableDashboardList(
                    keypath: "workItems.state.implementationGaps",
                    selectionStateKeypath: "workItems.state.selectedItemID",
                    selectionActionKeypath: "workItems.select",
                    rowSkeleton: havenWorkbenchWorkItemRowSkeleton()
                )
            ]
        )
    }

    private static func havenWorkbenchQuickActionsCard() -> SkeletonElement {
        catalogCardSection(
            "Quick actions",
            content: [
                dashboardStaticText("Disse lager en canonical WorkItem med trygg default-prioritet. Legg evidens i selected item etterpaa."),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            catalogButton(
                                keypath: "workItems.capture",
                                label: "Bug follow-up",
                                payload: .object([
                                    "title": .string("Ny bug follow-up"),
                                    "kind": .string("bug"),
                                    "priority": .string("P2"),
                                    "confidence": .string("needs-verification"),
                                    "labels": .list([.string("bug"), .string("haven-workbench")])
                                ])
                            ),
                            catalogButton(
                                keypath: "workItems.capture",
                                label: "Feature follow-up",
                                payload: .object([
                                    "title": .string("Ny feature follow-up"),
                                    "kind": .string("feature"),
                                    "priority": .string("P3"),
                                    "confidence": .string("needs-verification"),
                                    "labels": .list([.string("feature"), .string("haven-workbench")])
                                ])
                            )
                        ],
                        spacing: 8
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchProjectStatusCard() -> SkeletonElement {
        catalogCardSection(
            "Portfolio snapshot",
            content: [
                dashboardKeyText("projectPortfolio.state.summaryText", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("projectPortfolio.state.activeCount"),
                dashboardKeyText("projectPortfolio.state.riskCount"),
                dashboardKeyText("projectPortfolio.state.blockedCount"),
                dashboardKeyText("projectPortfolio.state.upcomingCount"),
                dashboardKeyText("projectPortfolio.state.overdueCount"),
                dashboardKeyText("projectPortfolio.state.openMilestoneCount"),
                dashboardKeyText("projectPortfolio.state.selectedProject.name", fontSize: 14, foregroundColor: "#8DE1DA"),
                dashboardKeyText("projectPortfolio.state.selectedProject.planningText", fontSize: 12, foregroundColor: "#9AC4CF"),
                dashboardKeyText("projectPortfolio.state.selectedProject.nextAction", fontSize: 12),
                dashboardKeyText("workItems.state.totalCount"),
                dashboardKeyText("workItems.state.openCount"),
                dashboardKeyText("serviceCatalog.state.serviceCount"),
                dashboardKeyText("serviceCatalog.state.implementationQueueCount"),
                dashboardKeyText("draftVersions.state.draftCount"),
                dashboardKeyText("draftVersions.state.versionCount"),
                dashboardStaticText("ProjectPortfolio er canonical prosjektoversikt i V0.5. Planleggingsdatoer, milestones, releases, capacity, saved views og native timeline/Gantt visualisering finnes naa.")
            ]
        )
    }

    private static func havenWorkbenchProjectIntakeCard() -> SkeletonElement {
        catalogCardSection(
            "Project intake",
            content: [
                dashboardStaticText("Fang nye prosjekter med status, helse, prioritet, owner-ref og planleggingsdatoer. Lenker til repo/celler/work items og milestones kan legges til via ProjectPortfolioCell-actions."),
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "projectPortfolio.state.captureDraft.name",
                        targetKeypath: "projectPortfolio.setDraftName",
                        placeholder: "Prosjektnavn"
                    )
                ),
                .TextArea(
                    SkeletonTextArea(
                        sourceKeypath: "projectPortfolio.state.captureDraft.summary",
                        targetKeypath: "projectPortfolio.setDraftSummary",
                        placeholder: "Hva skal prosjektet eie, hvorfor finnes det, og hva er neste trygge steg?",
                        minLines: 5,
                        maxLines: 12,
                        submitOnEnter: false,
                        editorMode: .richMarkdown
                    )
                ),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            .TextField(
                                SkeletonTextField(
                                    sourceKeypath: "projectPortfolio.state.captureDraft.startDate",
                                    targetKeypath: "projectPortfolio.setDraftStartDate",
                                    placeholder: "Start YYYY-MM-DD"
                                )
                            ),
                            .TextField(
                                SkeletonTextField(
                                    sourceKeypath: "projectPortfolio.state.captureDraft.targetDate",
                                    targetKeypath: "projectPortfolio.setDraftTargetDate",
                                    placeholder: "Target YYYY-MM-DD"
                                )
                            )
                        ],
                        spacing: 8
                    )
                ),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            havenWorkbenchProjectStatusPicker(),
                            havenWorkbenchProjectHealthPicker(),
                            havenWorkbenchProjectPriorityPicker()
                        ],
                        spacing: 8
                    )
                ),
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "projectPortfolio.state.captureDraft.ownerRef",
                        targetKeypath: "projectPortfolio.setDraftOwnerRef",
                        placeholder: "Owner ref"
                    )
                ),
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "projectPortfolio.state.captureDraft.currentFocus",
                        targetKeypath: "projectPortfolio.setDraftCurrentFocus",
                        placeholder: "Current focus"
                    )
                ),
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "projectPortfolio.state.captureDraft.nextAction",
                        targetKeypath: "projectPortfolio.setDraftNextAction",
                        placeholder: "Next action"
                    )
                ),
                ideaTaskActionButton(keypath: "projectPortfolio.captureDraft", label: "Fang prosjekt", emphasis: true)
            ]
        )
    }

    private static func havenWorkbenchProjectListCard(_ title: String, keypath: String) -> SkeletonElement {
        catalogCardSection(
            title,
            content: [
                selectableDashboardList(
                    keypath: keypath,
                    selectionStateKeypath: "projectPortfolio.state.selectedProjectID",
                    selectionActionKeypath: "projectPortfolio.select",
                    rowSkeleton: havenWorkbenchProjectRowSkeleton()
                )
            ]
        )
    }

    private static func projectPortfolioRoadmapTableCard() -> SkeletonElement {
        catalogCardSection(
            "Roadmap Gantt",
            content: [
                dashboardStaticText("Native Gantt-visning over start/target, release-lanes, status, helse, prioritet og neste milestone. Tabell ligger under som presis fallback."),
                .Visualization(
                    SkeletonVisualization(
                        kind: "gantt",
                        keypath: "projectPortfolio.state.roadmapItems",
                        stateKeypath: "projectPortfolio.state.selectedProjectID",
                        actionKeypath: "projectPortfolio.select"
                    )
                ),
                .Visualization(
                    SkeletonVisualization(
                        kind: "table",
                        keypath: "projectPortfolio.state.roadmapTable",
                        stateKeypath: "projectPortfolio.state.selectedProjectID",
                        actionKeypath: "projectPortfolio.select"
                    )
                )
            ]
        )
    }

    private static func projectPortfolioMilestoneTimelineCard() -> SkeletonElement {
        catalogCardSection(
            "Milestone timeline",
            content: [
                dashboardKeyText("projectPortfolio.state.openMilestoneCount", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                .Visualization(
                    SkeletonVisualization(
                        kind: "timeline",
                        keypath: "projectPortfolio.state.milestoneTimeline",
                        stateKeypath: "projectPortfolio.state.selectedProjectID",
                        actionKeypath: "projectPortfolio.select"
                    )
                ),
                .Visualization(
                    SkeletonVisualization(
                        kind: "table",
                        keypath: "projectPortfolio.state.milestoneTable",
                        stateKeypath: "projectPortfolio.state.selectedProjectID",
                        actionKeypath: "projectPortfolio.select"
                    )
                )
            ]
        )
    }

    private static func projectPortfolioActivityCard() -> SkeletonElement {
        catalogCardSection(
            "Activity",
            content: [
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "projectPortfolio.feed",
                        flowElementSkeleton: havenWorkbenchProjectActivityRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchServiceCatalogCard() -> SkeletonElement {
        catalogCardSection(
            "Service catalog",
            content: [
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "serviceCatalog.state.descriptors",
                        flowElementSkeleton: havenWorkbenchServiceRowSkeleton()
                    )
                ),
                dashboardKeyText("serviceCatalog.state.selectedService.serviceID", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("serviceCatalog.state.selectedService.purpose", fontSize: 12),
                dashboardKeyText("serviceCatalog.state.selectedService.requiresImplementation", fontSize: 12, foregroundColor: "#F6C66F")
            ]
        )
    }

    private static func havenWorkbenchImplementationQueueCard() -> SkeletonElement {
        catalogCardSection(
            "Neste implementeringssteg",
            content: [
                dashboardStaticText("Forslag og mangler som ServiceCatalog har funnet. Dette er ikke jobber som kjører automatisk.", fontSize: 12, foregroundColor: "#9AC4CF"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "serviceCatalog.state.implementationQueue",
                        flowElementSkeleton: havenWorkbenchImplementationQueueRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchDraftsCard() -> SkeletonElement {
        catalogCardSection(
            "Drafts / versions",
            content: [
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "draftVersions.state.drafts",
                        flowElementSkeleton: havenWorkbenchDraftRowSkeleton()
                    )
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "draftVersions.state.versions",
                        flowElementSkeleton: havenWorkbenchVersionRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchRelationMapCard() -> SkeletonElement {
        catalogCardSection(
            "HAVEN knowledge graph",
            content: [
                dashboardKeyText("graph.graph.explorer.state.summaryText", fontSize: 13, foregroundColor: "#9AC4CF"),
                .Visualization(
                    SkeletonVisualization(
                        kind: "network",
                        keypath: "graph.graph.explorer.state",
                        stateKeypath: "graph.graph.explorer.state.selectedID",
                        actionKeypath: "graph.graph.explorer.selectNode"
                    )
                ),
                dashboardKeyText("graph.graph.explorer.state.selectedNode.label", fontSize: 16, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("graph.graph.explorer.state.selectedNode.subtitle", fontSize: 12, foregroundColor: "#9AC4CF"),
                .Visualization(
                    SkeletonVisualization(
                        kind: "table",
                        keypath: "graph.graph.explorer.state.selectedEdges",
                        stateKeypath: "graph.graph.explorer.state.selectedID"
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchGraphStoreCard() -> SkeletonElement {
        catalogCardSection(
            "GraphStore",
            content: [
                dashboardKeyText("graph.graph.state.storageMode"),
                dashboardKeyText("graph.graph.state.nodeCount"),
                dashboardKeyText("graph.graph.state.edgeCount"),
                dashboardKeyText("graph.graph.state.operations"),
                dashboardStaticText("WorkItem og ProjectPortfolio sender relation updates til GraphStore via graph.workbench.applyUpdates.")
            ]
        )
    }

    private static func havenWorkbenchCoverageChartCard() -> SkeletonElement {
        catalogCardSection(
            "V0 coverage",
            content: [
                .Visualization(
                    SkeletonVisualization(
                        kind: "chart",
                        spec: .object([
                            "style": .string("bar"),
                            "rows": .list([
                                .object(["id": .string("intake"), "label": .string("Intake"), "value": .integer(4)]),
                                .object(["id": .string("triage"), "label": .string("Triage"), "value": .integer(3)]),
                                .object(["id": .string("backlog"), "label": .string("Backlog"), "value": .integer(3)]),
                                .object(["id": .string("planning"), "label": .string("Planning"), "value": .integer(2)]),
                                .object(["id": .string("collab"), "label": .string("Collab"), "value": .integer(1)])
                            ])
                        ])
                    )
                ),
                dashboardStaticText("Timeline/Gantt er bevisst ikke en egen renderer-kind i V0.")
            ]
        )
    }

    private static func havenWorkbenchDocsCard() -> SkeletonElement {
        catalogCardSection(
            "Docs og RAG",
            content: [
                dashboardKeyText("rag.state.setup.statusLabel"),
                dashboardKeyText("rag.state.currentCase"),
                dashboardKeyText("rag.state.queryAnswer"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "rag.state.queryCitations",
                        flowElementSkeleton: havenWorkbenchCitationRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchAICard() -> SkeletonElement {
        catalogCardSection(
            "AI sidevogn",
            content: [
                dashboardKeyText("aiGateway.state.setup.statusLabel"),
                .TextArea(
                    SkeletonTextArea(
                        sourceKeypath: "aiGateway.state.draft.prompt",
                        targetKeypath: "aiGateway.setDraftPrompt",
                        placeholder: "Be om triage, dublettsjekk, neste steg eller bug-repro. AI maa ikke skrive canonical state uten eksplisitt brukerhandling.",
                        minLines: 6,
                        maxLines: 12,
                        submitOnEnter: false
                    )
                ),
                catalogButton(keypath: "aiGateway.invokeDraft", label: "Invoke advisory AI"),
                dashboardKeyText("aiGateway.state.lastInvocation.outputPreview")
            ]
        )
    }

    private static func havenWorkbenchKnownGapsCard() -> SkeletonElement {
        catalogCardSection(
            "Bevisste gap",
            content: [
                dashboardStaticText("Canonical WorkItemCell, ProjectPortfolioCell og GitHubWorkSyncCell finnes naa med state-first sync, mutation acks og Flow-events. Roadmap har read-only Gantt/timeline med tabellfallback, men ikke drag/edit."),
                dashboardStaticText("Todo er fortsatt personlig execution, Vault er evidens/notater, ProjectOperations er service-/implementation-katalog, GraphStore er bredere relasjoner."),
                dashboardStaticText("Assistenter skal bruke haven-work-intake-skillen for aa legge inn arbeid som tydelige ideer/notater/tasks med evidens og trygg neste handling.")
            ]
        )
    }

    private static func havenWorkbenchSyncStatusCard() -> SkeletonElement {
        catalogCardSection(
            "Sync status",
            content: [
                dashboardStaticText("Canonical flow: klienten henter state foerst, abonnerer paa Flow-events, og bruker eventsSince ved replay/resync."),
                dashboardKeyText("workItems.state.stateVersion", fontSize: 14, fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("workItems.state.syncStatus.mode", fontSize: 12, foregroundColor: "#9AC4CF"),
                dashboardKeyText("workItems.state.syncStatus.eventsAvailable", fontSize: 12),
                dashboardKeyText("projectPortfolio.state.stateVersion", fontSize: 14, fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("projectPortfolio.state.syncStatus.eventsAvailable", fontSize: 12),
                dashboardKeyText("githubSync.state.stateVersion", fontSize: 14, fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("githubSync.state.syncStatus.eventsAvailable", fontSize: 12)
            ]
        )
    }

    private static func havenWorkbenchSavedViewsCard() -> SkeletonElement {
        catalogCardSection(
            "Saved views",
            content: [
                dashboardKeyText("projectPortfolio.state.savedViewCount", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardStaticText("Shared portfolio filters for needs-triage, blocked, stale, overdue og risk. Work-item filter views bruker dagens state-lister inntil egne view records trengs."),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "projectPortfolio.state.savedViews",
                        flowElementSkeleton: havenWorkbenchSavedViewRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func projectPortfolioReleaseCard() -> SkeletonElement {
        catalogCardSection(
            "Releases",
            content: [
                dashboardKeyText("projectPortfolio.state.releaseCount", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "projectPortfolio.state.releases",
                        flowElementSkeleton: havenWorkbenchReleaseRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func projectPortfolioCapacityCard() -> SkeletonElement {
        catalogCardSection(
            "Capacity / workload",
            content: [
                dashboardKeyText("projectPortfolio.state.workloadSummary.capacityPoints", fontSize: 14, fontWeight: "semibold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("projectPortfolio.state.workloadSummary.allocatedPoints", fontSize: 14, foregroundColor: "#F6C66F"),
                dashboardKeyText("projectPortfolio.state.workloadSummary.remainingPoints", fontSize: 14, foregroundColor: "#8DE1DA"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "projectPortfolio.state.capacity",
                        flowElementSkeleton: havenWorkbenchCapacityRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func githubWorkSyncStatusCard() -> SkeletonElement {
        catalogCardSection(
            "GitHub sync",
            content: [
                dashboardStaticText("Import/read-sync er lokal og trygg. Ekstern write-back ligger i outbound-ko og krever eksplisitt handling utenfor denne importen."),
                dashboardKeyText("githubSync.state.externalWriteMode", fontSize: 14, fontWeight: "semibold", foregroundColor: "#F6C66F"),
                dashboardKeyText("githubSync.state.repoCount"),
                dashboardKeyText("githubSync.state.importedItemCount"),
                dashboardKeyText("githubSync.state.outboundQueueCount"),
                dashboardKeyText("githubSync.state.syncStatus.mode", fontSize: 12, foregroundColor: "#9AC4CF"),
                dashboardKeyText("githubSync.state.syncStatus.eventsAvailable", fontSize: 12)
            ]
        )
    }

    private static func githubWorkSyncRepoCard() -> SkeletonElement {
        catalogCardSection(
            "Repo mapping",
            content: [
                dashboardKeyText("githubSync.state.repoMappingStatus", fontSize: 14, fontWeight: "semibold", foregroundColor: "#8DE1DA"),
                dashboardKeyText("githubSync.state.repoMappingSummary", fontSize: 12, foregroundColor: "#D5E4ED"),
                dashboardKeyText("githubSync.state.repoMappingNextAction", fontSize: 12, foregroundColor: "#9AC4CF"),
                dashboardKeyText("githubSync.state.repoMappingWriteBoundary", fontSize: 12, foregroundColor: "#F6C66F"),
                catalogButton(
                    keypath: "githubSync.configureRepo",
                    label: "Add/update HAVEN repo mapping",
                    payload: .object([
                        "repoID": .string("Digipomps/HAVEN"),
                        "owner": .string("Digipomps"),
                        "name": .string("HAVEN"),
                        "defaultProject": .string("HAVEN Workbench"),
                        "labelStatusMap": .object([
                            "bug": .string("triage"),
                            "blocked": .string("blocked")
                        ]),
                        "labelPriorityMap": .object([
                            "P0": .string("P0"),
                            "P1": .string("P1"),
                            "critical": .string("P0")
                        ])
                    ])
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "githubSync.state.repos",
                        flowElementSkeleton: githubWorkSyncRepoRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func githubWorkSyncImportCard() -> SkeletonElement {
        catalogCardSection(
            "Imports",
            content: [
                catalogButton(
                    keypath: "githubSync.importFixture",
                    label: "Import fixture",
                    payload: .object([
                        "repositories": .list([
                            .object([
                                "repoID": .string("Digipomps/HAVEN"),
                                "owner": .string("Digipomps"),
                                "name": .string("HAVEN"),
                                "defaultProject": .string("HAVEN Workbench")
                            ])
                        ]),
                        "issues": .list([
                            .object([
                                "repoID": .string("Digipomps/HAVEN"),
                                "number": .integer(1),
                                "title": .string("Example imported issue"),
                                "state": .string("open"),
                                "labels": .list([.string("bug"), .string("P2")]),
                                "url": .string("https://github.com/Digipomps/HAVEN/issues/1")
                            ])
                        ]),
                        "pullRequests": .list([
                            .object([
                                "repoID": .string("Digipomps/HAVEN"),
                                "number": .integer(2),
                                "title": .string("Example imported PR"),
                                "state": .string("open"),
                                "labels": .list([.string("feature")]),
                                "ciStatus": .string("pending"),
                                "url": .string("https://github.com/Digipomps/HAVEN/pull/2")
                            ])
                        ])
                    ])
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "githubSync.state.imports",
                        flowElementSkeleton: githubWorkSyncImportRowSkeleton()
                    )
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "githubSync.state.workItemPayloads",
                        flowElementSkeleton: githubWorkSyncPayloadRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func githubWorkSyncOutboundCard() -> SkeletonElement {
        catalogCardSection(
            "Explicit outbound",
            content: [
                catalogButton(
                    keypath: "githubSync.queueOutboundIssue",
                    label: "Queue write-back",
                    payload: .object([
                        "repoID": .string("Digipomps/HAVEN"),
                        "action": .string("create-or-update-issue"),
                        "workItemID": .string("manual-work-item-id"),
                        "title": .string("Queued outbound issue"),
                        "body": .string("Requires explicit user approval before external write.")
                    ])
                ),
                catalogButton(keypath: "githubSync.clearOutboundQueue", label: "Clear queue", payload: .object([:])),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "githubSync.state.outboundQueue",
                        flowElementSkeleton: githubWorkSyncOutboundRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchSavedViewRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("scope", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("sort", fontSize: 12),
            dashboardKeyText("filters", fontSize: 12, foregroundColor: "#9AC4CF"),
            .Divider(SkeletonDivider())
        ])
    }

    private static func havenWorkbenchReleaseRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("status", fontSize: 12, foregroundColor: "#F6C66F"),
            dashboardKeyText("targetDate", fontSize: 12, foregroundColor: "#9AC4CF"),
            dashboardKeyText("projectCount", fontSize: 12),
            dashboardKeyText("workItemCount", fontSize: 12),
            .Divider(SkeletonDivider())
        ])
    }

    private static func havenWorkbenchCapacityRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("scopeRef", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("period", fontSize: 12, foregroundColor: "#9AC4CF"),
            dashboardKeyText("capacityPoints", fontSize: 12),
            dashboardKeyText("allocatedPoints", fontSize: 12, foregroundColor: "#F6C66F"),
            dashboardKeyText("remainingPoints", fontSize: 12, foregroundColor: "#8DE1DA"),
            .Divider(SkeletonDivider())
        ])
    }

    private static func githubWorkSyncRepoRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("mappingTitle", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("projectText", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("labelStatusText", fontSize: 12, foregroundColor: "#9AC4CF"),
            dashboardKeyText("labelPriorityText", fontSize: 12, foregroundColor: "#9AC4CF"),
            dashboardKeyText("mappingSummary", fontSize: 12),
            dashboardKeyText("nextAction", fontSize: 12, foregroundColor: "#F6C66F"),
            .Divider(SkeletonDivider())
        ])
    }

    private static func githubWorkSyncImportRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("kind", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("state", fontSize: 12, foregroundColor: "#F6C66F"),
            dashboardKeyText("labelText", fontSize: 12, foregroundColor: "#9AC4CF"),
            dashboardKeyText("ciStatus", fontSize: 12),
            dashboardKeyText("workItemID", fontSize: 12),
            .Divider(SkeletonDivider())
        ])
    }

    private static func githubWorkSyncPayloadRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("kind", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("status", fontSize: 12, foregroundColor: "#F6C66F"),
            dashboardKeyText("priority", fontSize: 12),
            dashboardKeyText("repo", fontSize: 12, foregroundColor: "#9AC4CF"),
            .Divider(SkeletonDivider())
        ])
    }

    private static func githubWorkSyncOutboundRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("action", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("repoID", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("workItemID", fontSize: 12),
            dashboardKeyText("status", fontSize: 12, foregroundColor: "#F6C66F"),
            dashboardKeyText("requiresExplicitUserAction", fontSize: 12, foregroundColor: "#9AC4CF"),
            .Divider(SkeletonDivider())
        ])
    }

    private static func havenWorkbenchWorkItemKindPicker() -> SkeletonElement {
        var picker = SkeletonPicker(
            label: "Type",
            placeholder: "Velg type",
            elements: [
                .object(["id": .string("idea"), "title": .string("Idea")]),
                .object(["id": .string("feature"), "title": .string("Feature")]),
                .object(["id": .string("bug"), "title": .string("Bug")]),
                .object(["id": .string("chore"), "title": .string("Chore")]),
                .object(["id": .string("docs"), "title": .string("Docs")]),
                .object(["id": .string("research"), "title": .string("Research")]),
                .object(["id": .string("decision"), "title": .string("Decision")]),
                .object(["id": .string("question"), "title": .string("Question")]),
                .object(["id": .string("implementation-gap"), "title": .string("Implementation gap")])
            ],
            optionLabelKeypath: "title",
            selectionValueKeypath: "id",
            selectionStateKeypath: "workItems.state.captureDraft.kind",
            selectionActionKeypath: "workItems.setDraftKind",
            selectionPayloadMode: .itemID,
            allowsEmptySelection: false
        )
        var modifiers = SkeletonModifiers()
        modifiers.styleClasses = ["work-item-kind-picker"]
        picker.modifiers = modifiers
        return .Picker(picker)
    }

    private static func havenWorkbenchProjectStatusPicker() -> SkeletonElement {
        havenWorkbenchProjectPicker(
            label: "Status",
            placeholder: "Status",
            elements: [
                ("new", "New"),
                ("planning", "Planning"),
                ("active", "Active"),
                ("paused", "Paused"),
                ("blocked", "Blocked"),
                ("done", "Done"),
                ("archived", "Archived")
            ],
            selectionStateKeypath: "projectPortfolio.state.captureDraft.status",
            selectionActionKeypath: "projectPortfolio.setDraftStatus"
        )
    }

    private static func havenWorkbenchProjectHealthPicker() -> SkeletonElement {
        havenWorkbenchProjectPicker(
            label: "Health",
            placeholder: "Health",
            elements: [
                ("green", "Green"),
                ("yellow", "Yellow"),
                ("red", "Red"),
                ("unknown", "Unknown")
            ],
            selectionStateKeypath: "projectPortfolio.state.captureDraft.health",
            selectionActionKeypath: "projectPortfolio.setDraftHealth"
        )
    }

    private static func havenWorkbenchProjectPriorityPicker() -> SkeletonElement {
        havenWorkbenchProjectPicker(
            label: "Priority",
            placeholder: "Priority",
            elements: [
                ("P0", "P0"),
                ("P1", "P1"),
                ("P2", "P2"),
                ("P3", "P3"),
                ("P4", "P4")
            ],
            selectionStateKeypath: "projectPortfolio.state.captureDraft.priority",
            selectionActionKeypath: "projectPortfolio.setDraftPriority"
        )
    }

    private static func havenWorkbenchProjectPicker(
        label: String,
        placeholder: String,
        elements: [(String, String)],
        selectionStateKeypath: String,
        selectionActionKeypath: String
    ) -> SkeletonElement {
        var picker = SkeletonPicker(
            label: label,
            placeholder: placeholder,
            elements: elements.map { .object(["id": .string($0.0), "title": .string($0.1)]) },
            optionLabelKeypath: "title",
            selectionValueKeypath: "id",
            selectionStateKeypath: selectionStateKeypath,
            selectionActionKeypath: selectionActionKeypath,
            selectionPayloadMode: .itemID,
            allowsEmptySelection: false
        )
        var modifiers = SkeletonModifiers()
        modifiers.styleClasses = ["project-portfolio-picker"]
        picker.modifiers = modifiers
        return .Picker(picker)
    }

    private static func havenWorkbenchProjectRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("name", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("status", fontSize: 12, foregroundColor: "#F6C66F"),
            dashboardKeyText("health", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("priority", fontSize: 12),
            dashboardKeyText("repoText", fontSize: 12, foregroundColor: "#9AC4CF"),
            dashboardKeyText("cellText", fontSize: 12, foregroundColor: "#9AC4CF"),
            dashboardKeyText("workItemCount", fontSize: 12),
            dashboardKeyText("planningText", fontSize: 12, foregroundColor: "#9AC4CF"),
            dashboardKeyText("milestoneCount", fontSize: 12),
            dashboardKeyText("nextMilestoneTitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("currentFocus", fontSize: 12),
            dashboardKeyText("nextAction", fontSize: 12),
            .Divider(SkeletonDivider())
        ])
    }

    private static func havenWorkbenchProjectActivityRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("summary", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("kind", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("field", fontSize: 12),
            dashboardKeyText("toValue", fontSize: 12, foregroundColor: "#F6C66F"),
            .Divider(SkeletonDivider())
        ])
    }

    private static func havenWorkbenchBoardSurface() -> SkeletonElement {
        let lanes: [(status: String, title: String, compact: Bool)] = [
            ("new", "Inbox", false),
            ("triage", "Triage", false),
            ("ready", "Ready", false),
            ("in-progress", "In progress", false),
            ("blocked", "Blocked", false),
            ("done", "Done", true),
            ("wont-do", "Won't do", true)
        ]

        var boardScrollModifiers = SkeletonModifiers()
        boardScrollModifiers.styleRole = "work-board-scroll"
        boardScrollModifiers.styleClasses = ["haven-work-board-scroll"]

        var boardGridModifiers = SkeletonModifiers()
        boardGridModifiers.styleRole = "work-board-grid"
        boardGridModifiers.styleClasses = ["haven-work-board-grid"]

        let boardGrid = SkeletonGrid(
            columns: lanes.map { _ in .fixed(296) },
            spacing: 12,
            elements: lanes.map { lane in
                lane.compact
                    ? havenWorkbenchBoardCompactLane(status: lane.status, title: lane.title)
                    : havenWorkbenchBoardLane(status: lane.status, title: lane.title)
            },
            modifiers: boardGridModifiers
        )

        var boardScroll = SkeletonScrollView(axis: "horizontal", elements: [
            .Grid(boardGrid)
        ])
        boardScroll.modifiers = boardScrollModifiers

        var boardBaseModifiers = SkeletonModifiers()
        boardBaseModifiers.styleRole = "work-board-base"
        boardBaseModifiers.styleClasses = ["haven-work-board-base"]

        var boardOverlayModifiers = SkeletonModifiers()
        boardOverlayModifiers.styleRole = "work-board-overlay"
        boardOverlayModifiers.styleClasses = ["haven-work-board-overlay"]

        var surfaceModifiers = SkeletonModifiers()
        surfaceModifiers.styleRole = "work-board-surface"
        surfaceModifiers.styleClasses = ["haven-work-board-surface"]

        return .VStack(
            SkeletonVStack(
                elements: [
                    havenWorkbenchBoardToolbar(),
                    .VStack(
                        SkeletonVStack(
                            elements: [
                                .VStack(
                                    SkeletonVStack(
                                        elements: [.ScrollView(boardScroll)],
                                        modifiers: boardBaseModifiers
                                    )
                                )
                            ],
                            modifiers: boardOverlayModifiers
                        )
                    )
                ],
                spacing: 12,
                modifiers: surfaceModifiers
            )
        )
    }

    private static func havenWorkbenchBoardToolbar() -> SkeletonElement {
        var titleFieldModifiers = SkeletonModifiers()
        titleFieldModifiers.styleClasses = ["haven-work-board-title-input"]
        titleFieldModifiers.padding = 8
        titleFieldModifiers.cornerRadius = 6
        titleFieldModifiers.borderWidth = 1
        titleFieldModifiers.borderColor = "#315064"

        return catalogCardSection(
            "Board",
            content: [
                .HStack(
                    SkeletonHStack(
                        elements: [
                            dashboardBadgeKeyText("workItems.state.summaryText"),
                            dashboardBadgeKeyText("workItems.state.board.selectedLaneID"),
                            dashboardBadgeKeyText("workItems.state.board.sortMode"),
                            catalogButton(
                                keypath: "ownerSetup.seedOwnerWorkbench",
                                label: "Sett opp min Workbench",
                                payload: .object(["source": .string("haven-workbench-board-toolbar")])
                            )
                        ],
                        spacing: 8
                    )
                ),
                .TextField(
                    SkeletonTextField(
                        sourceKeypath: "workItems.state.captureDraft.title",
                        targetKeypath: "workItems.setDraftTitle",
                        placeholder: "Ny work item",
                        modifiers: titleFieldModifiers
                    )
                )
            ]
        )
    }

    private static func havenWorkbenchBoardLane(status: String, title: String) -> SkeletonElement {
        var laneModifiers = havenWorkbenchBoardLaneModifiers(status: status)
        laneModifiers.styleClasses = ["haven-work-board-lane", "haven-work-board-lane-\(status.replacingOccurrences(of: "-", with: ""))"]

        var section = SkeletonSection(
            header: havenWorkbenchBoardLaneHeader(status: status, title: title),
            footer: havenWorkbenchBoardQuickAddButton(status: status, title: title),
            content: [
                selectableDashboardList(
                    keypath: "workItems.state.board.\(status).items",
                    selectionStateKeypath: "workItems.state.selectedItemID",
                    selectionActionKeypath: "workItems.select",
                    rowSkeleton: havenWorkbenchBoardCardSkeleton(),
                    styleClasses: ["haven-work-board-card-list"]
                )
            ]
        )
        section.modifiers = laneModifiers
        return .Section(section)
    }

    private static func havenWorkbenchBoardCompactLane(status: String, title: String) -> SkeletonElement {
        var laneModifiers = havenWorkbenchBoardLaneModifiers(status: status)
        laneModifiers.styleClasses = ["haven-work-board-lane", "haven-work-board-compact-lane"]

        var section = SkeletonSection(
            header: havenWorkbenchBoardLaneHeader(status: status, title: title),
            footer: havenWorkbenchBoardQuickAddButton(status: status, title: title),
            content: [
                dashboardKeyText("workItems.state.board.\(status).collapsedSummary", fontSize: 13, foregroundColor: "#9AC4CF")
            ]
        )
        section.modifiers = laneModifiers
        return .Section(section)
    }

    private static func havenWorkbenchBoardLaneHeader(status: String, title: String) -> SkeletonElement {
        .HStack(
            SkeletonHStack(
                elements: [
                    dashboardStaticText(title, fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                    dashboardBadgeKeyText("workItems.state.board.\(status).count")
                ],
                spacing: 8
            )
        )
    }

    private static func havenWorkbenchBoardQuickAddButton(status: String, title: String) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.styleClasses = ["haven-work-board-quick-add"]
        modifiers.padding = 8
        modifiers.cornerRadius = 6
        modifiers.borderWidth = 1
        modifiers.borderColor = "#315064"
        modifiers.background = "#102635"
        modifiers.foregroundColor = "#C6F5EE"
        var button = SkeletonButton(
            keypath: "workItems.captureDraft",
            label: "+ \(title)",
            payload: .object(["status": .string(status)])
        )
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func havenWorkbenchBoardLaneModifiers(status: String) -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 10
        modifiers.background = "#0B1821"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#244457"
        modifiers.dropTargetRole = "work-status:\(status)"
        modifiers.acceptedDragRoles = ["work-item-card"]
        modifiers.dropActionKeypath = "workItems.board.dropCard"
        modifiers.dropIntents = ["move"]
        modifiers.dropValidationStateKeypath = "workItems.state.board.\(status).dropValidationState"
        modifiers.dropDeniedReasonKeypath = "workItems.state.board.\(status).dropDeniedReason"
        modifiers.accessibilityDropLabel = "Drop work item on \(status)"
        return modifiers
    }

    private static func havenWorkbenchBoardCardSkeleton() -> SkeletonVStack {
        var cardModifiers = SkeletonModifiers()
        cardModifiers.styleClasses = ["haven-work-board-card"]
        cardModifiers.padding = 10
        cardModifiers.background = "#F8FAFC"
        cardModifiers.cornerRadius = 8
        cardModifiers.borderWidth = 1
        cardModifiers.borderColor = "#CBD5E1"
        cardModifiers.draggableRole = "work-item-card"
        cardModifiers.dragPayloadKeypath = "id"
        cardModifiers.dragPreviewRole = "work-item-card"
        cardModifiers.accessibilityDragLabel = "Drag work item card"

        return SkeletonVStack(
            elements: [
                havenWorkbenchBoardCardDropZone(role: "work-card-before"),
                dashboardKeyText("title", fontSize: 14, fontWeight: "bold", foregroundColor: "#0F1B24"),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            havenWorkbenchBoardChip("kind", color: "#0F766E"),
                            havenWorkbenchBoardChip("priority", color: "#B91C1C"),
                            havenWorkbenchBoardChip("project", color: "#334155")
                        ],
                        spacing: 6
                    )
                ),
                dashboardKeyText("nextAction", fontSize: 12, foregroundColor: "#334155"),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            havenWorkbenchBoardChip("blockerCount", color: "#B91C1C"),
                            havenWorkbenchBoardChip("commentCount", color: "#2563EB"),
                            havenWorkbenchBoardChip("subtaskCount", color: "#047857")
                        ],
                        spacing: 6
                    )
                ),
                havenWorkbenchBoardCardDropZone(role: "work-card-after")
            ],
            spacing: 6,
            modifiers: cardModifiers
        )
    }

    private static func havenWorkbenchBoardChip(_ keypath: String, color: String) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 5
        modifiers.background = "#FFFFFF"
        modifiers.cornerRadius = 6
        modifiers.borderWidth = 1
        modifiers.borderColor = "#E2E8F0"
        modifiers.foregroundColor = color
        modifiers.fontSize = 11
        modifiers.fontWeight = "semibold"
        modifiers.styleClasses = ["haven-work-board-chip"]
        var element = SkeletonText(keypath: keypath)
        element.modifiers = modifiers
        return .Text(element)
    }

    private static func havenWorkbenchBoardCardDropZone(role: String) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.height = 6
        modifiers.cornerRadius = 3
        modifiers.dropTargetRole = role
        modifiers.acceptedDragRoles = ["work-item-card"]
        modifiers.dropActionKeypath = "workItems.board.dropCard"
        modifiers.dropIntents = ["move"]
        modifiers.dropTargetPayloadKeypath = "id"
        modifiers.dropValidationStateKeypath = "workItems.state.board.ready.dropValidationState"
        modifiers.accessibilityDropLabel = "Drop work item \(role.contains("before") ? "before" : "after") this card"
        modifiers.styleClasses = ["haven-work-board-card-drop-zone"]
        var section = SkeletonSection(content: [])
        section.modifiers = modifiers
        return .Section(section)
    }

    private static func havenWorkbenchSelectedWorkItemPanel() -> SkeletonElement {
        var closeButtonModifiers = SkeletonModifiers()
        closeButtonModifiers.styleClasses = ["haven-work-board-detail-close"]
        closeButtonModifiers.padding = 7
        closeButtonModifiers.cornerRadius = 6
        closeButtonModifiers.borderWidth = 1
        closeButtonModifiers.borderColor = "#315064"
        closeButtonModifiers.background = "#102635"
        closeButtonModifiers.foregroundColor = "#C6F5EE"

        var closeButton = SkeletonButton(
            keypath: "workItems.clearSelection",
            label: "Lukk",
            payload: .object(["source": .string("haven-work-board-detail")])
        )
        closeButton.modifiers = closeButtonModifiers

        var drawerModifiers = SkeletonModifiers()
        drawerModifiers.styleRole = "work-board-detail-drawer"
        drawerModifiers.styleClasses = ["haven-work-board-detail-drawer"]
        drawerModifiers.padding = 14
        drawerModifiers.background = "#0F1B24"
        drawerModifiers.cornerRadius = 12
        drawerModifiers.borderWidth = 1
        drawerModifiers.borderColor = "#244457"
        drawerModifiers.shadowRadius = 28
        drawerModifiers.shadowX = 0
        drawerModifiers.shadowY = 20
        drawerModifiers.shadowColor = "rgba(0, 0, 0, 0.34)"
        drawerModifiers.visibility = SkeletonVisibilityRule(
            when: SkeletonCondition(
                keypath: "workItems.state.selectedItemIsOpen",
                equals: .bool(true)
            )
        )
        drawerModifiers.presentation = SkeletonPresentation(
            kind: .drawer,
            placement: .trailing,
            closeActionKeypath: "workItems.clearSelection",
            openStateKeypath: "workItems.state.selectedItemIsOpen",
            dismissOnBackdrop: true,
            backdropStyle: .dim,
            escapeKeyBehavior: .closeAction,
            focusTrap: false,
            anchorRole: "work-item-card",
            anchorKeypath: "workItems.state.selectedItemID",
            zIndex: 30,
            mobileFallback: SkeletonPresentationFallback(kind: .sheet, placement: .bottom),
            accessibilityLabel: "Work item details"
        )

        var headerModifiers = SkeletonModifiers()
        headerModifiers.styleClasses = ["haven-work-board-detail-header"]

        var section = SkeletonSection(
            header: .HStack(
                SkeletonHStack(
                    elements: [
                        dashboardStaticText("Card Details", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                        .Spacer(SkeletonSpacer()),
                        .Button(closeButton)
                    ],
                    spacing: 8,
                    modifiers: headerModifiers
                )
            ),
            content: [
                dashboardKeyText("workItems.state.selectedItem.title", fontSize: 18, fontWeight: "bold", foregroundColor: "#F5FBFF"),
                dashboardKeyText("workItems.state.selectedItem.summary", fontSize: 13, foregroundColor: "#D5E4ED"),
                .HStack(
                    SkeletonHStack(
                        elements: [
                            dashboardBadgeKeyText("workItems.state.selectedItem.kind"),
                            dashboardBadgeKeyText("workItems.state.selectedItem.status"),
                            dashboardBadgeKeyText("workItems.state.selectedItem.priority"),
                            dashboardBadgeKeyText("workItems.state.selectedItem.project")
                        ],
                        spacing: 8
                    )
                ),
                dashboardKeyText("workItems.state.selectedItem.nextAction", fontSize: 13, foregroundColor: "#8DE1DA"),
                dashboardKeyText("workItems.state.selectedItem.doneWhen", fontSize: 13, foregroundColor: "#F6C66F"),
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 140, max: 220)],
                        spacing: 8,
                        elements: [
                            dashboardBadgeKeyText("workItems.state.selectedItem.evidenceCount"),
                            dashboardBadgeKeyText("workItems.state.selectedItem.relationshipCount"),
                            dashboardBadgeKeyText("workItems.state.selectedItem.commentCount"),
                            dashboardBadgeKeyText("workItems.state.selectedItem.subtaskCount")
                        ]
                    )
                ),
                dashboardStaticText("Workflow", fontSize: 12, fontWeight: "semibold", foregroundColor: "#9AC4CF"),
                .List(
                    styledDashboardList(
                        keypath: "workItems.state.selectedItem.statusActions",
                        rowSkeleton: havenWorkbenchSelectedWorkItemActionRowSkeleton(actionKeypath: "workItems.setStatus"),
                        styleClasses: ["haven-work-board-detail-actions"]
                    )
                ),
                dashboardStaticText("Priority", fontSize: 12, fontWeight: "semibold", foregroundColor: "#9AC4CF"),
                .List(
                    styledDashboardList(
                        keypath: "workItems.state.selectedItem.priorityActions",
                        rowSkeleton: havenWorkbenchSelectedWorkItemActionRowSkeleton(actionKeypath: "workItems.setPriority"),
                        styleClasses: ["haven-work-board-detail-actions"]
                    )
                ),
                dashboardStaticText("Ownership and planning", fontSize: 12, fontWeight: "semibold", foregroundColor: "#9AC4CF"),
                dashboardKeyText("workItems.state.selectedItem.assignee", fontSize: 12, foregroundColor: "#D5E4ED"),
                dashboardKeyText("workItems.state.selectedItem.teamRef", fontSize: 12, foregroundColor: "#D5E4ED"),
                dashboardKeyText("workItems.state.selectedItem.labelText", fontSize: 12, foregroundColor: "#9AC4CF"),
                dashboardKeyText("workItems.state.selectedItem.dueDate", fontSize: 12, foregroundColor: "#F6C66F"),
                dashboardStaticText("Dependencies", fontSize: 12, fontWeight: "semibold", foregroundColor: "#9AC4CF"),
                dashboardKeyText("workItems.state.selectedItem.blockedByRefs", fontSize: 12, foregroundColor: "#F6C66F"),
                dashboardKeyText("workItems.state.selectedItem.blocksRefs", fontSize: 12, foregroundColor: "#8DE1DA"),
                .List(
                    styledDashboardList(
                        keypath: "workItems.state.selectedItem.relationships",
                        rowSkeleton: havenWorkbenchSelectedWorkItemRelationshipRowSkeleton(),
                        styleClasses: ["haven-work-board-detail-list"]
                    )
                ),
                dashboardStaticText("Comments", fontSize: 12, fontWeight: "semibold", foregroundColor: "#9AC4CF"),
                .List(
                    styledDashboardList(
                        keypath: "workItems.state.selectedItem.comments",
                        rowSkeleton: havenWorkbenchSelectedWorkItemCommentRowSkeleton(),
                        styleClasses: ["haven-work-board-detail-list"]
                    )
                ),
                dashboardStaticText("Subtasks", fontSize: 12, fontWeight: "semibold", foregroundColor: "#9AC4CF"),
                .List(
                    styledDashboardList(
                        keypath: "workItems.state.selectedItem.subtasks",
                        rowSkeleton: havenWorkbenchSelectedWorkItemSubtaskRowSkeleton(),
                        styleClasses: ["haven-work-board-detail-list"]
                    )
                ),
                dashboardStaticText("Evidence", fontSize: 12, fontWeight: "semibold", foregroundColor: "#9AC4CF"),
                .List(
                    styledDashboardList(
                        keypath: "workItems.state.selectedItem.evidence",
                        rowSkeleton: havenWorkbenchSelectedWorkItemEvidenceRowSkeleton(),
                        styleClasses: ["haven-work-board-detail-list"]
                    )
                ),
                dashboardStaticText("Activity", fontSize: 12, fontWeight: "semibold", foregroundColor: "#9AC4CF"),
                .List(
                    styledDashboardList(
                        keypath: "workItems.state.selectedItem.recentActivity",
                        rowSkeleton: havenWorkbenchSelectedWorkItemActivityRowSkeleton(),
                        styleClasses: ["haven-work-board-detail-list"]
                    )
                )
            ]
        )
        section.modifiers = drawerModifiers
        return .Section(section)
    }

    private static func havenWorkbenchSelectedWorkItemCommentRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(
            elements: [
                dashboardKeyText("body", fontSize: 12, foregroundColor: "#F5FBFF"),
                dashboardKeyText("source", fontSize: 11, foregroundColor: "#9AC4CF")
            ],
            spacing: 4
        )
    }

    private static func havenWorkbenchSelectedWorkItemSubtaskRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(
            elements: [
                dashboardKeyText("title", fontSize: 12, foregroundColor: "#F5FBFF"),
                dashboardKeyText("isDone", fontSize: 11, foregroundColor: "#9AC4CF")
            ],
            spacing: 4
        )
    }

    private static func havenWorkbenchSelectedWorkItemEvidenceRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(
            elements: [
                dashboardKeyText("summary", fontSize: 12, foregroundColor: "#F5FBFF"),
                dashboardKeyText("source", fontSize: 11, foregroundColor: "#9AC4CF")
            ],
            spacing: 4
        )
    }

    private static func havenWorkbenchSelectedWorkItemRelationshipRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(
            elements: [
                dashboardKeyText("normalizedKind", fontSize: 11, foregroundColor: "#8DE1DA"),
                dashboardKeyText("targetRef", fontSize: 12, foregroundColor: "#F5FBFF"),
                dashboardKeyText("summary", fontSize: 11, foregroundColor: "#9AC4CF")
            ],
            spacing: 4
        )
    }

    private static func havenWorkbenchSelectedWorkItemActivityRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(
            elements: [
                dashboardKeyText("summary", fontSize: 12, foregroundColor: "#F5FBFF"),
                dashboardKeyText("kind", fontSize: 11, foregroundColor: "#8DE1DA"),
                dashboardKeyText("actorRef", fontSize: 11, foregroundColor: "#9AC4CF")
            ],
            spacing: 4
        )
    }

    private static func havenWorkbenchSelectedWorkItemActionRowSkeleton(actionKeypath: String) -> SkeletonVStack {
        var button = SkeletonButton(
            keypath: actionKeypath,
            label: "Update",
            labelKeypath: "label",
            payloadKeypath: "payload"
        )
        var modifiers = SkeletonModifiers()
        modifiers.styleClasses = ["haven-work-board-detail-action"]
        modifiers.padding = 7
        modifiers.cornerRadius = 6
        modifiers.borderWidth = 1
        modifiers.borderColor = "#315064"
        modifiers.background = "#102635"
        modifiers.foregroundColor = "#C6F5EE"
        button.modifiers = modifiers
        return SkeletonVStack(elements: [.Button(button)])
    }

    private static func havenWorkbenchWorkItemRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("kind", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("status", fontSize: 12, foregroundColor: "#F6C66F"),
            dashboardKeyText("priority", fontSize: 12),
            dashboardKeyText("project", fontSize: 12, foregroundColor: "#9AC4CF"),
            dashboardKeyText("blockerCount", fontSize: 12, foregroundColor: "#F6C66F"),
            dashboardKeyText("blockingCount", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("blockedByRefs", fontSize: 12, foregroundColor: "#F6C66F"),
            dashboardKeyText("blocksRefs", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("commentCount", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("activityCount", fontSize: 12, foregroundColor: "#9AC4CF"),
            dashboardKeyText("nextAction", fontSize: 12),
            .Divider(SkeletonDivider())
        ])
    }

    private static func havenWorkbenchServiceRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("serviceID", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("owningCell", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("purpose", fontSize: 12),
            .Divider(SkeletonDivider())
        ])
    }

    private static func havenWorkbenchImplementationQueueRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            .HStack(SkeletonHStack(elements: [
                dashboardStaticText("Status:", fontSize: 12, foregroundColor: "#9AC4CF"),
                dashboardKeyText("status", fontSize: 12, foregroundColor: "#F6C66F")
            ])),
            dashboardKeyText("summary", fontSize: 12),
            .HStack(SkeletonHStack(elements: [
                dashboardStaticText("Tilhører:", fontSize: 12, foregroundColor: "#9AC4CF"),
                dashboardKeyText("serviceID", fontSize: 12, foregroundColor: "#9AC4CF")
            ])),
            .Divider(SkeletonDivider())
        ])
    }

    private static func havenWorkbenchDraftRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("draftID", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subjectKind", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("status", fontSize: 12),
            .Divider(SkeletonDivider())
        ])
    }

    private static func havenWorkbenchVersionRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("versionID", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subjectKind", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("commitMessage", fontSize: 12),
            .Divider(SkeletonDivider())
        ])
    }

    private static func havenWorkbenchCitationRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 14, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("source", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("url", fontSize: 12),
            .Divider(SkeletonDivider())
        ])
    }

    static func obsidianMermaidStagingConfiguration() -> CellConfiguration {
        var configuration = CellConfiguration(name: "Staging Demo (Obsidian + Mermaid)")
        configuration.description = "Kombinert staging-oppsett med Vault-kontrakt og Mermaid-rendering i samme skeleton."
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///Vault",
            sourceCellName: "VaultCell",
            purpose: "Staging demo for Vault og Mermaid",
            purposeDescription: "Kombinert notat- og diagramarbeidsflate som viser hvordan flere cellereferanser kan brukes i én web-klar konfigurasjon.",
            interests: ["staging", "vault", "obsidian", "mermaid", "diagram", "demo"],
            menuSlots: ["upperLeft", "lowerLeft"]
        )

        var vaultReference = CellReference(endpoint: "cell:///Vault", label: "vault")
        vaultReference.setKeysAndValues = [KeyValue(key: "vault.note.list", value: .object(vaultListNotesPayload(tags: ["staging"], limit: 10)))]
        configuration.addReference(vaultReference)

        var mermaidReference = CellReference(endpoint: "cell:///MermaidRenderer", label: "mermaidRenderer")
        mermaidReference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(mermaidReference)

        var elements = SkeletonElementList()
        elements.append(catalogText("Staging Demo (Obsidian + Mermaid)"))
        elements.append(catalogText("Samlet skeleton for notatflyt og diagramrendering. Vault-delen følger API/cell-kontrakten, mens Mermaid-delen gir både preset-actions og fri kilde-input."))
        elements.append(contentsOf: vaultWorkspaceSections(
            referenceLabel: "vault",
            primaryNoteID: stagingVaultPrimaryNoteID,
            linkedNoteID: stagingVaultLinkedNoteID,
            listPayload: vaultListNotesPayload(tags: ["staging"], limit: 10),
            createPrimaryPayload: vaultCreateNotePayload(
                id: stagingVaultPrimaryNoteID,
                title: "Staging Mermaid note",
                content: "Note generated from combined staging config.",
                tags: ["staging", "obsidian", "mermaid"]
            ),
            createLinkedPayload: vaultCreateNotePayload(
                id: stagingVaultLinkedNoteID,
                title: "Staging Mermaid linked note",
                content: "Linked follow-up note for staging demo.",
                tags: ["staging", "obsidian"]
            ),
            updatePrimaryPayload: vaultUpdateNotePayload(
                id: stagingVaultPrimaryNoteID,
                title: "Staging Mermaid note (updated)",
                content: "Updated from the combined staging skeleton.",
                tags: ["staging", "obsidian", "mermaid", "updated"]
            ),
            getPrimaryPayload: vaultGetNotePayload(id: stagingVaultPrimaryNoteID),
            linkPayload: vaultAddLinkPayload(fromNoteID: stagingVaultPrimaryNoteID, toNoteID: stagingVaultLinkedNoteID)
        ))
        elements.append(contentsOf: mermaidRendererSections(
            referenceLabel: "mermaidRenderer",
            sampleSource: stagingMermaidSampleSource,
            svgPayload: mermaidWebViewSVGPayload(
                source: stagingMermaidSampleSource,
                correlationId: "staging-combined-mermaid-svg"
            ),
            pngPayload: mermaidWebViewPNGPayload(
                source: stagingMermaidSampleSource,
                correlationId: "staging-combined-mermaid-png"
            ),
            nativePayload: mermaidNativePNGPayload(
                source: stagingMermaidSampleSource,
                correlationId: "staging-combined-mermaid-native"
            )
        ))

        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    private static let mermaidPlaygroundSampleSource = """
    flowchart TD
    Input["Input"] --> Renderer["MermaidRendererCell"]
    Renderer --> SVG["SVG output"]
    Renderer --> PNG["PNG output"]
    """

    private static let conferenceOwnershipDocID = "book-17-conference-ownership-dataflow"

    private static let stagingMermaidSampleSource = """
    flowchart TD
    Vault["Vault note"] --> Renderer["MermaidRenderer"]
    Renderer --> Diagram["Diagram output"]
    """

    private static let defaultVaultPrimaryNoteID = "obsidian-sample-001"
    private static let defaultVaultLinkedNoteID = "obsidian-sample-002"
    private static let obsidianAIVaultPrimaryNoteID = "obsidian-ai-note-001"
    private static let obsidianAIVaultLinkedNoteID = "obsidian-ai-note-002"
    private static let stagingVaultPrimaryNoteID = "staging-mermaid-note-001"
    private static let stagingVaultLinkedNoteID = "staging-mermaid-note-002"
    private static let conferenceParticipantPortalLoadConfigurationName = "Conference Participant Portal Dashboard"
    private static let conferenceParticipantPortalLoadSourceCellEndpoint = "cell:///ConferenceParticipantPreviewShell"
    private static let defaultVaultPrimaryContent = """
    # Mermaid + Vault

    ```mermaid
    flowchart TD
    A-->B
    ```
    """
    private static let obsidianAIVaultPrimaryContent = """
    # Obsidian AI Workspace

    Notes from a research session:

    - tighten the current idea into a sharper outline
    - identify likely backlinks
    - extract next concrete steps
    """

    private static func mermaidRendererSections(
        referenceLabel: String,
        sampleSource: String,
        svgPayload: Object,
        pngPayload: Object,
        nativePayload: Object
    ) -> SkeletonElementList {
        [
            catalogSection(
                "Interactive Source",
                content: [
                    catalogText("Rediger diagramkilden og bruk Cmd/Ctrl+Enter for å sende tekstfeltet direkte til `render.mermaid` som standard webview SVG-render."),
                    .TextArea(
                        SkeletonTextArea(
                            text: sampleSource,
                            sourceKeypath: nil,
                            targetKeypath: "\(referenceLabel).render.mermaid",
                            placeholder: "flowchart TD\\nA-->B",
                            minLines: 8,
                            maxLines: 18,
                            submitOnEnter: false
                        )
                    )
                ]
            ),
            catalogSection(
                "Preset Actions",
                content: [
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "\(referenceLabel).render.mermaid",
                                label: "Render SVG (webview)",
                                payload: .object(svgPayload)
                            ),
                            catalogButton(
                                keypath: "\(referenceLabel).render.mermaid",
                                label: "Render PNG (webview)",
                                payload: .object(pngPayload)
                            ),
                            catalogButton(
                                keypath: "\(referenceLabel).render.mermaid",
                                label: "Render PNG (native)",
                                payload: .object(nativePayload)
                            )
                        ])
                    )
                ]
            ),
            catalogSection(
                "Rendered Diagram",
                content: [
                    catalogText("Preview-feltet under viser faktisk rendret SVG/PNG i web. Binding viser fallback/status på samme sted hvis klienten ikke kan vise HTML-bildet direkte."),
                    catalogRenderedHTML("\(referenceLabel).state.last_render.rendered_html")
                ]
            ),
            catalogSection(
                "Runtime State",
                content: [
                    catalogKeyText("\(referenceLabel).state.status"),
                    catalogKeyText("\(referenceLabel).state.endpoint"),
                    catalogKeyText("\(referenceLabel).state.capability"),
                    catalogKeyText("\(referenceLabel).state.renderTimeoutMs"),
                    catalogKeyText("\(referenceLabel).state.cacheEntries"),
                    catalogKeyText("\(referenceLabel).state.maxCacheEntries"),
                    catalogKeyText("\(referenceLabel).state.totalRenders"),
                    catalogKeyText("\(referenceLabel).state.cacheHits"),
                    catalogKeyText("\(referenceLabel).state.webViewRuntimeAvailable"),
                    catalogKeyText("\(referenceLabel).state.nativeRuntimeAvailable"),
                    catalogKeyText("\(referenceLabel).state.lastError")
                ]
            ),
            catalogSection(
                "Last Render",
                content: [
                    catalogText("Siste render-respons speiles inn i `state.lastRender`. SVG-tekst preview er avkortet for å holde skeleton-responsen lesbar."),
                    catalogKeyText("\(referenceLabel).state.lastRender.hasResult"),
                    catalogKeyText("\(referenceLabel).state.lastRender.correlationId"),
                    catalogKeyText("\(referenceLabel).state.lastRender.sourcePreview"),
                    catalogKeyText("\(referenceLabel).state.lastRender.backend"),
                    catalogKeyText("\(referenceLabel).state.lastRender.output"),
                    catalogKeyText("\(referenceLabel).state.lastRender.cacheHit"),
                    catalogKeyText("\(referenceLabel).state.lastRender.renderTimeMs"),
                    catalogKeyText("\(referenceLabel).state.lastRender.engineVersion"),
                    catalogKeyText("\(referenceLabel).state.lastRender.contentHash"),
                    catalogKeyText("\(referenceLabel).state.lastRender.pngBytesCount"),
                    catalogKeyText("\(referenceLabel).state.lastRender.renderedImageKind"),
                    catalogKeyText("\(referenceLabel).state.lastRender.renderedImageAvailable"),
                    catalogKeyText("\(referenceLabel).state.lastRender.warningsText"),
                    catalogKeyText("\(referenceLabel).state.lastRender.errorsText"),
                    catalogKeyText("\(referenceLabel).state.lastRender.svgTextPreview")
                ]
            )
        ]
    }

    private static func conferenceOwnershipDiagramSections(referenceLabel: String) -> SkeletonElementList {
        [
            catalogSection(
                "Actions",
                content: [
                    catalogText("Render book-dokumentet på nytt ved behov. Web-backend viser ferdig HTML med inline Mermaid-SVG, mens swift-backend brukes for blokkstruktur og parity."),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "\(referenceLabel).render.markdown",
                                label: "Render web doc",
                                payload: .object(conferenceOwnershipDiagramRenderPayload(backend: .web))
                            ),
                            catalogButton(
                                keypath: "\(referenceLabel).render.markdown",
                                label: "Render swift blocks",
                                payload: .object(conferenceOwnershipDiagramRenderPayload(backend: .swift))
                            )
                        ])
                    )
                ]
            ),
            catalogSection(
                "Document State",
                content: [
                    catalogKeyText("\(referenceLabel).state.status"),
                    catalogKeyText("\(referenceLabel).state.endpoint"),
                    catalogKeyText("\(referenceLabel).state.document_count"),
                    catalogKeyText("\(referenceLabel).state.entry_doc_id"),
                    catalogKeyText("\(referenceLabel).state.render_count"),
                    catalogKeyText("\(referenceLabel).state.last_error"),
                    catalogKeyText("\(referenceLabel).state.last_render.status"),
                    catalogKeyText("\(referenceLabel).state.last_render.backend"),
                    catalogKeyText("\(referenceLabel).state.last_render.doc_id"),
                    catalogKeyText("\(referenceLabel).state.last_render.title"),
                    catalogKeyText("\(referenceLabel).state.last_render.source_path"),
                    catalogKeyText("\(referenceLabel).state.last_render.web_url"),
                    catalogKeyText("\(referenceLabel).state.last_render.mermaid_block_count"),
                    catalogKeyText("\(referenceLabel).state.last_render.heading_count"),
                    catalogKeyText("\(referenceLabel).state.last_render.warning_text"),
                    catalogKeyText("\(referenceLabel).state.last_render.error_text")
                ]
            ),
            catalogSection(
                "Rendered Documentation",
                content: [
                    catalogText("HTML-fragmentet under kommer direkte fra `state.lastRender.renderedHTML`. Hvis dokumentet ble rendret med web-backend vil Mermaid-diagrammet vises inline her."),
                    catalogRenderedHTML("\(referenceLabel).state.last_render.rendered_html")
                ]
            )
        ]
    }

    private static func vaultWorkspaceSections(
        referenceLabel: String,
        primaryNoteID: String,
        linkedNoteID: String,
        listPayload: Object,
        createPrimaryPayload: Object,
        createLinkedPayload: Object,
        updatePrimaryPayload: Object,
        getPrimaryPayload: Object,
        linkPayload: Object
    ) -> SkeletonElementList {
        [
            catalogSection(
                "Vault Actions",
                content: [
                    catalogText("Denne skeletonen fokuserer på de eksplisitte set/get-operasjonene som web/API-laget bruker: create, update, get, list og link."),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "\(referenceLabel).vault.note.create",
                                label: "Create primary note",
                                payload: .object(createPrimaryPayload)
                            ),
                            catalogButton(
                                keypath: "\(referenceLabel).vault.note.create",
                                label: "Create linked note",
                                payload: .object(createLinkedPayload)
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "\(referenceLabel).vault.note.update",
                                label: "Update primary note",
                                payload: .object(updatePrimaryPayload)
                            ),
                            catalogButton(
                                keypath: "\(referenceLabel).vault.note.get",
                                label: "Get primary note",
                                payload: .object(getPrimaryPayload)
                            )
                        ])
                    ),
                    .HStack(
                        SkeletonHStack(elements: [
                            catalogButton(
                                keypath: "\(referenceLabel).vault.note.list",
                                label: "List notes",
                                payload: .object(listPayload)
                            ),
                            catalogButton(
                                keypath: "\(referenceLabel).vault.link.add",
                                label: "Create wiki link",
                                payload: .object(linkPayload)
                            )
                        ])
                    )
                ]
            ),
            catalogSection(
                "Contract Notes",
                content: [
                    catalogText("Primary note id: \(primaryNoteID)"),
                    catalogText("Linked note id: \(linkedNoteID)"),
                    catalogText("Exposed methods: `vault.note.create`, `vault.note.update`, `vault.note.get`, `vault.note.list`, `vault.link.add`."),
                    catalogText("Hvis `cell:///Vault` ikke er registrert i runtime vil knappene ikke få svar, selv om `/vault/api/*` fortsatt kan fungere via API-bridge fallback.")
                ]
            )
        ]
    }

    private static func catalogText(_ text: String) -> SkeletonElement {
        var skeletonText = SkeletonText(text: text)
        var modifiers = SkeletonModifiers()
        modifiers.foregroundColor = "#D5E4ED"
        skeletonText.modifiers = modifiers
        return .Text(skeletonText)
    }

    private static func catalogKeyText(_ keypath: String) -> SkeletonElement {
        var skeletonText = SkeletonText(keypath: keypath)
        var modifiers = SkeletonModifiers()
        modifiers.foregroundColor = "#D5E4ED"
        skeletonText.modifiers = modifiers
        return .Text(skeletonText)
    }

    private static func catalogRenderedHTML(_ keypath: String) -> SkeletonElement {
        var text = SkeletonText(keypath: keypath)
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "rendered-html"
        text.modifiers = modifiers
        return .Text(text)
    }

    private static func catalogButton(keypath: String, label: String, payload: ValueType? = .bool(true)) -> SkeletonElement {
        .Button(SkeletonButton(keypath: keypath, label: label, payload: payload))
    }

    private static func catalogSection(_ title: String, content: SkeletonElementList) -> SkeletonElement {
        var headerText = SkeletonText(text: title)
        var headerModifiers = SkeletonModifiers()
        headerModifiers.foregroundColor = "#D5E4ED"
        headerText.modifiers = headerModifiers
        return .Section(
            SkeletonSection(
                header: .Text(headerText),
                content: content
            )
        )
    }

    private static func adminScaffoldConnectionBanner(connected: Bool) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.cornerRadius = 10
        modifiers.borderWidth = 1
        modifiers.background = connected ? "#12352E" : "#4A1F24"
        modifiers.borderColor = connected ? "#5FC8A7" : "#FF9AA8"
        modifiers.visibility = SkeletonVisibilityRule(
            when: SkeletonCondition(
                scope: .root,
                keypath: "adminOverview.connected",
                equals: .bool(connected)
            )
        )

        let content: SkeletonElementList
        if connected {
            content = [
                catalogText("AdminScaffold er tilkoblet. Kontroller tidspunkt og readiness før du handler."),
                catalogKeyText("adminOverview.state.timestamp"),
                catalogKeyText("adminOverview.state.deployment.readiness")
            ]
        } else {
            content = [
                catalogText("AdminScaffold er utilgjengelig. Ingen lokale vertsdata vises."),
                catalogText("Kontroller TLS, bridge-legitimasjon, Agreement og rollecredential. Webcontaineren faller ikke tilbake til lokal runtime- eller Docker-tilgang.")
            ]
        }

        var section = SkeletonSection(content: content)
        section.modifiers = modifiers
        return .Section(section)
    }

    private static func catalogCardSection(_ title: String, content: SkeletonElementList) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.background = "#0F1B24"
        modifiers.cornerRadius = 12
        modifiers.borderWidth = 1
        modifiers.borderColor = "#1F3442"

        var headerText = SkeletonText(text: title)
        var headerModifiers = SkeletonModifiers()
        headerModifiers.foregroundColor = "#D5E4ED"
        headerText.modifiers = headerModifiers

        var section = SkeletonSection(
            header: .Text(headerText),
            content: content
        )
        section.modifiers = modifiers
        return .Section(section)
    }

    private static func participantPortalHeroSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Portal Header",
            content: [
                .HStack(
                    SkeletonHStack(
                        elements: [
                            .VStack(
                                SkeletonVStack(elements: [
                                    dashboardStaticText(
                                        "DELTAGERPORTAL",
                                        fontSize: 12,
                                        fontWeight: "bold",
                                        foregroundColor: "#7FD6D0"
                                    ),
                                    dashboardKeyText(
                                        "\(referenceLabel).state.workspace.title",
                                        fontSize: 20,
                                        fontWeight: "bold",
                                        foregroundColor: "#F5FBFF"
                                    ),
                                    dashboardKeyText(
                                        "\(referenceLabel).state.workspace.subtitle",
                                        fontSize: 13,
                                        foregroundColor: "#D5E4ED"
                                    )
                                ])
                            ),
                            .Spacer(SkeletonSpacer()),
                            .VStack(
                                SkeletonVStack(elements: [
                                    dashboardBadgeKeyText("\(referenceLabel).state.workspace.participantBadge"),
                                    dashboardBadgeKeyText("\(referenceLabel).state.workspace.conferenceBadge")
                                ])
                            )
                        ]
                    )
                ),
                dashboardKeyText(
                    "\(referenceLabel).state.workspace.nextStep",
                    fontSize: 13,
                    foregroundColor: "#D7E7F2"
                ),
                dashboardStaticText("Live pulse"),
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 220, max: 300)],
                        spacing: 12,
                        keypath: "\(referenceLabel).state.workspace.pulseCards",
                        itemSkeleton: dashboardMetricCardSkeleton()
                    )
                ),
                dashboardKeyText(
                    "\(referenceLabel).state.workspace.previewNotice",
                    fontSize: 12,
                    foregroundColor: "#D5E4ED"
                )
            ]
        )
    }

    private static func participantPortalAgendaSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Min Agenda",
            content: [
                dashboardKeyText("\(referenceLabel).state.program.intro"),
                dashboardKeyText("\(referenceLabel).state.program.nextAction"),
                dashboardKeyText("\(referenceLabel).state.program.agendaSummary"),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "agenda.setView",
                            label: "Se anbefalte",
                            payload: .object(["view": .string("forYou")])
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "agenda.setView",
                            label: "Se alt",
                            payload: .object(["view": .string("timeline")])
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "agenda.setView",
                            label: "Se valgte",
                            payload: .object(["view": .string("saved")])
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "agenda.setView",
                            label: "Fra valgte spor",
                            payload: .object(["view": .string("focusedTracks")])
                        )
                    ])
                ),
                dashboardStaticText("Spor"),
                selectableDashboardList(
                    keypath: "\(referenceLabel).state.program.trackOptions",
                    selectionStateKeypath: "\(referenceLabel).state.program.selectedTrackID",
                    selectionActionKeypath: "\(referenceLabel).agenda.selectTrack",
                    rowSkeleton: dashboardAgendaTrackCardRowSkeleton(),
                    styleClasses: ["conference-agenda-track-grid", "conference-agenda-card-list"]
                ),
                dashboardStaticText("Valgt spor"),
                dashboardKeyText("\(referenceLabel).state.program.selectedTrack.title"),
                dashboardKeyText("\(referenceLabel).state.program.selectedTrack.subtitle"),
                dashboardKeyText("\(referenceLabel).state.program.selectedTrack.detail"),
                dashboardKeyText("\(referenceLabel).state.program.selectedTrack.note"),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "agenda.toggleSelectedTrackFocus",
                            label: "Fokus valgt spor"
                        ),
                        loadConfigurationButton(
                            "Åpne spor-detaljer",
                            configurationName: "Conference Agenda Track Detail",
                            sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell"
                        )
                    ])
                ),
                dashboardKeyText("\(referenceLabel).state.program.viewSummary"),
                dashboardKeyText("\(referenceLabel).state.program.timelineSummary"),
                dashboardKeyText("\(referenceLabel).state.program.layoutSummary"),
                dashboardKeyText("\(referenceLabel).state.program.status"),
                dashboardStaticText("Tidsslots"),
                .List(
                    styledDashboardList(
                        keypath: "\(referenceLabel).state.program.timeSlotRows",
                        rowSkeleton: dashboardAgendaTimeSlotMatrixRowSkeleton(referenceLabel: referenceLabel),
                        styleClasses: ["conference-agenda-timeslot-list"]
                    )
                ),
                dashboardStaticText("Valgt sesjon"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.title"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.subtitle"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.detail"),
                dashboardKeyText("\(referenceLabel).state.program.selectedSession.note"),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "agenda.toggleSelectedSessionSaved",
                            label: "Lagre/fjern valgt"
                        ),
                        loadConfigurationButton(
                            "Åpne sesjonsdetaljer",
                            configurationName: "Conference Agenda Session Detail",
                            sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell"
                        )
                    ])
                ),
                dashboardKeyText("\(referenceLabel).state.program.storageSummary")
            ]
        )
    }

    private static func participantPortalValueStorySection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Din verdi og deling",
            content: [
                dashboardKeyText("\(referenceLabel).state.valueStory.intro"),
                dashboardKeyText("\(referenceLabel).state.valueStory.nextAction"),
                dashboardStaticText("Grafiske summary-kort som også fungerer i Binding"),
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 220, max: 320)],
                        spacing: 12,
                        keypath: "\(referenceLabel).state.valueStory.graphCards",
                        itemSkeleton: dashboardMetricCardSkeleton()
                    )
                ),
                dashboardKeyText("\(referenceLabel).state.valueStory.personalBenefitSummary"),
                dashboardKeyText("\(referenceLabel).state.valueStory.sharedBoundarySummary"),
                dashboardKeyText("\(referenceLabel).state.valueStory.organizerVisibilitySummary"),
                dashboardKeyText("\(referenceLabel).state.valueStory.sponsorVisibilitySummary"),
                dashboardStaticText("Det som skal være lett å si høyt i demoen"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.valueStory.evidenceRows",
                        flowElementSkeleton: dashboardConnectionRowSkeleton()
                    )
                )
            ]
        )
    }

    private static func participantPortalRecommendationsSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Dine Personlige Anbefalinger",
            content: [
                dashboardKeyText("\(referenceLabel).state.matches.intro"),
                dashboardKeyText("\(referenceLabel).state.matches.filterSummary"),
                dashboardKeyText("\(referenceLabel).state.matches.status"),
                dashboardKeyText("\(referenceLabel).state.matches.recommendationSummary"),
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 220, max: 320)],
                        spacing: 12,
                        keypath: "\(referenceLabel).state.matches.recommendations",
                        itemSkeleton: dashboardRecommendationCardSkeleton()
                    )
                ),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "matchmaking.refreshRecommendations",
                            label: "Oppdater treff"
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "matchmaking.setFilters",
                            label: "Bytt filter"
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "matchmaking.searchPeople",
                            label: "Søk governance",
                            payload: .object(["query": .string("governance")])
                        )
                    ])
                )
            ]
        )
    }

    private static func participantPortalHappyPathSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Safest Live Path",
            content: [
                dashboardStaticText("1. Velg en sterk kandidat fra anbefalingene over og trykk Start chat direkte på kortet."),
                dashboardStaticText("2. Når chaten er startet, åpne den dedikerte chatflaten og send én kort oppfølging."),
                dashboardStaticText("3. Bytt deretter til control tower og pek på den samme shared follow-up-virkeligheten."),
                dashboardKeyText("\(referenceLabel).state.discovery.nextAction"),
                dashboardKeyText("\(referenceLabel).state.chat.launchSummary"),
                dashboardKeyText("\(referenceLabel).state.chat.nextAction"),
                dashboardKeyText("\(referenceLabel).state.sharedConnections.chatSummary"),
                dashboardKeyText("\(referenceLabel).state.meetings.meetingSummary"),
                .HStack(
                    SkeletonHStack(elements: [
                        loadConfigurationButton("Åpne chatflate", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch"),
                        loadConfigurationButton("Åpne control tower", configurationName: "Conference Control Tower", sourceCellEndpoint: "cell:///ConferenceAdminPreviewShell"),
                        loadConfigurationButton("Åpne full preview", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint)
                    ])
                )
            ]
        )
    }

    private static func participantPortalTimelineSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Min Tidslinje",
            content: [
                dashboardKeyText("\(referenceLabel).state.meetings.intro"),
                dashboardKeyText("\(referenceLabel).state.meetings.requestSummary"),
                dashboardKeyText("\(referenceLabel).state.meetings.slotSummary"),
                dashboardKeyText("\(referenceLabel).state.meetings.meetingSummary"),
                dashboardKeyText("\(referenceLabel).state.meetings.exportStatus"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.meetings.confirmedMeetings",
                        flowElementSkeleton: dashboardTimelineRowSkeleton()
                    )
                ),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "scheduling.createMeetingRequest",
                            label: "Be om møte",
                            payload: .object(["source": .string("participant-portal-dashboard")])
                        )
                    ])
                )
            ]
        )
    }

    private static func participantPortalDiscoverySection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Oppdagelse",
            content: [
                dashboardKeyText("\(referenceLabel).state.discovery.intro"),
                dashboardKeyText("\(referenceLabel).state.discovery.status"),
                dashboardKeyText("\(referenceLabel).state.discovery.alignmentSummary"),
                dashboardKeyText("\(referenceLabel).state.discovery.proofSummary"),
                dashboardKeyText("\(referenceLabel).state.discovery.publicProfileSummary"),
                dashboardKeyText("\(referenceLabel).state.discovery.chatSummary"),
                dashboardKeyText("\(referenceLabel).state.discovery.nextAction"),
                dashboardStaticText("Kandidater"),
                selectableDashboardList(
                    keypath: "\(referenceLabel).state.discovery.candidates",
                    selectionStateKeypath: "\(referenceLabel).state.discovery.selectedCandidateID",
                    selectionActionKeypath: "\(referenceLabel).discovery.selectCandidate",
                    rowSkeleton: dashboardDiscoveryCardSkeleton(),
                    styleClasses: ["conference-agenda-session-list", "conference-agenda-card-list", "conference-discovery-card-list"]
                ),
                dashboardStaticText("Valgt treff"),
                dashboardKeyText("\(referenceLabel).state.discovery.selectedCandidate.title"),
                dashboardKeyText("\(referenceLabel).state.discovery.selectedCandidate.subtitle"),
                dashboardKeyText("\(referenceLabel).state.discovery.selectedCandidate.detail"),
                dashboardKeyText("\(referenceLabel).state.discovery.selectedCandidate.note"),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "discovery.startChatWithSelectedCandidate",
                            label: "Legg til chat"
                        ),
                        loadConfigurationButton("Åpne chatflate", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch")
                    ])
                ),
                dashboardStaticText("Kompakt chat"),
                dashboardKeyText("\(referenceLabel).state.chat.launchSummary"),
                dashboardKeyText("\(referenceLabel).state.chat.conversationSummary"),
                dashboardKeyText("\(referenceLabel).state.chat.messageSummary"),
                dashboardKeyText("\(referenceLabel).state.chat.nextAction"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.chat.recentMessages",
                        flowElementSkeleton: dashboardMessageRowSkeleton()
                    )
                ),
                dashboardStaticText("Proof-klare treff"),
                selectableDashboardList(
                    keypath: "\(referenceLabel).state.discovery.proofCandidates",
                    selectionStateKeypath: "\(referenceLabel).state.discovery.selectedProofCandidateID",
                    selectionActionKeypath: "\(referenceLabel).discovery.selectProofCandidate",
                    rowSkeleton: dashboardProofDiscoveryCardSkeleton(),
                    styleClasses: ["conference-agenda-session-list", "conference-agenda-card-list", "conference-discovery-card-list", "conference-proof-card-list"]
                ),
                dashboardStaticText("Valgt proof-treff"),
                dashboardKeyText("\(referenceLabel).state.discovery.selectedProofCandidate.title"),
                dashboardKeyText("\(referenceLabel).state.discovery.selectedProofCandidate.subtitle"),
                dashboardKeyText("\(referenceLabel).state.discovery.selectedProofCandidate.detail"),
                dashboardKeyText("\(referenceLabel).state.discovery.selectedProofCandidate.note"),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "discovery.startProofChatWithSelectedCandidate",
                            label: "Start proof-chat med valgt person"
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "proofChat.generateArtifacts",
                            label: "Lag proof-artefakter"
                        )
                    ])
                ),
                dashboardStaticText("Kompakt proof-chat"),
                dashboardKeyText("\(referenceLabel).state.proofChat.launchSummary"),
                dashboardKeyText("\(referenceLabel).state.proofChat.status"),
                dashboardKeyText("\(referenceLabel).state.proofChat.invitationSummary"),
                dashboardKeyText("\(referenceLabel).state.proofChat.messageSummary"),
                dashboardKeyText("\(referenceLabel).state.proofChat.nextAction"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.proofChat.messages",
                        flowElementSkeleton: dashboardMessageRowSkeleton()
                    )
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.discovery.groupSuggestions",
                        flowElementSkeleton: dashboardDiscoveryRowSkeleton()
                    )
                ),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "discovery.refresh",
                            label: "Oppdater discovery"
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "discoveryChat.sendMessage",
                            label: "Send hei",
                            payload: .object(["text": .string("Hei! Skal vi fortsette konferansepraten her?")])
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "proofChat.sendMessage",
                            label: "Send proof-hei",
                            payload: .object(["text": .string("Hei! Dette er en proof-backed konferansechat.")])
                        )
                    ])
                )
            ]
        )
    }

    private static func participantPortalProofChatSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Proof Chat",
            content: [
                dashboardKeyText("\(referenceLabel).state.proofChat.intro"),
                dashboardKeyText("\(referenceLabel).state.proofChat.status"),
                dashboardKeyText("\(referenceLabel).state.proofChat.launchSummary"),
                dashboardKeyText("\(referenceLabel).state.proofChat.audienceSummary"),
                dashboardKeyText("\(referenceLabel).state.proofChat.invitationSummary"),
                dashboardKeyText("\(referenceLabel).state.proofChat.artifactSummary"),
                dashboardKeyText("\(referenceLabel).state.proofChat.cryptoSummary"),
                dashboardKeyText("\(referenceLabel).state.proofChat.nextAction"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.proofChat.targets",
                        flowElementSkeleton: dashboardConnectionRowSkeleton()
                    )
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.proofChat.invitations",
                        flowElementSkeleton: dashboardConnectionRowSkeleton()
                    )
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.proofChat.messages",
                        flowElementSkeleton: dashboardMessageRowSkeleton()
                    )
                ),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "proofChat.generateArtifacts",
                            label: "Lag artifacts"
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "proofChat.acceptFirstPendingInviteLocally",
                            label: "Godta lokalt"
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "proofChat.sendMessage",
                            label: "Send proof-hei",
                            payload: .object(["text": .string("Hei! Dette er en proof-backed konferansechat.")])
                        )
                    ])
                )
            ]
        )
    }

    private static func participantPortalDirectChatSection(referenceLabel: String) -> SkeletonElement {
        compactConferenceChatSection(
            title: "Direkte Chat",
            chatKeypathPrefix: "\(referenceLabel).state.chat",
            primaryButtons: [
                participantPortalActionButton(
                    referenceLabel,
                    actionKeypath: "discoveryChat.sendMessage",
                    label: "Send hei",
                    payload: .object(["text": .string("Hei! Skal vi fortsette praten her?")])
                ),
                participantPortalActionButton(
                    referenceLabel,
                    actionKeypath: "discoveryChat.sendMessage",
                    label: "Foreslå kaffe",
                    payload: .object(["text": .string("Skal vi finne et tidspunkt for kaffe etter neste sesjon?")])
                ),
                loadConfigurationButton("Åpne chatflate", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch")
            ]
        )
    }

    private static func conferenceParticipantPortalDemoFlowSection() -> SkeletonElement {
        catalogCardSection(
            "More Paths",
            content: [
                dashboardStaticText("Bruk disse hoppene når du vil åpne fordypningsflater eller bytte perspektiv uten å lete i Library."),
                .HStack(
                    SkeletonHStack(elements: [
                        loadConfigurationButton("Åpne full preview", configurationName: Self.conferenceParticipantPortalLoadConfigurationName, sourceCellEndpoint: Self.conferenceParticipantPortalLoadSourceCellEndpoint),
                        loadConfigurationButton("Åpne profile editor", configurationName: "Conference Public Profile Editor", sourceCellEndpoint: "cell:///ConferencePublicProfileEditorPreview"),
                        loadConfigurationButton("Åpne public profile", configurationName: "Conference Public Profile", sourceCellEndpoint: "cell:///ConferencePublicProfilePreview")
                    ])
                ),
                .HStack(
                    SkeletonHStack(elements: [
                        loadConfigurationButton("Åpne participant chat", configurationName: "Conference Participant Chat", sourceCellEndpoint: "cell:///ConferenceChatLaunch"),
                        loadConfigurationButton("Åpne control tower", configurationName: "Conference Control Tower", sourceCellEndpoint: "cell:///ConferenceAdminPreviewShell"),
                        loadConfigurationButton("Åpne demo launcher", configurationName: "Conference Demo Launcher", sourceCellEndpoint: "cell:///ConfigurationCatalog")
                    ])
                )
            ]
        )
    }

    private static func appendingSection(_ section: SkeletonElement, to configuration: CellConfiguration) -> CellConfiguration {
        var configuration = configuration
        guard case let .VStack(stack)? = configuration.skeleton else {
            return configuration
        }

        var elements = stack.elements
        elements.append(section)
        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    private static func detailConfiguration(
        name: String,
        description: String,
        titleKeypath: String,
        subtitleKeypath: String,
        detailKeypath: String,
        noteKeypath: String,
        primaryButtons: [SkeletonElement]
    ) -> CellConfiguration {
        var configuration = CellConfiguration(name: name)
        configuration.description = description
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferencePublicShell",
            sourceCellName: "ConferencePublicShellCell",
            purpose: name,
            purposeDescription: description,
            interests: ["conference", "public", "detail", "selection", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var reference = CellReference(endpoint: "cell:///ConferencePublicShell", subscribeFeed: false, label: "conferencePublicShell")
        reference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(reference)

        var elements = SkeletonElementList()
        elements.append(catalogText(name))
        elements.append(
            catalogCardSection(
                "Detail",
                content: [
                    dashboardKeyText(titleKeypath),
                    dashboardKeyText(subtitleKeypath),
                    dashboardKeyText(detailKeypath),
                    dashboardKeyText(noteKeypath),
                    .HStack(SkeletonHStack(elements: primaryButtons))
                ]
            )
        )
        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    private static func participantAgendaDetailConfiguration(
        name: String,
        description: String,
        titleKeypath: String,
        subtitleKeypath: String,
        detailKeypath: String,
        noteKeypath: String,
        extraContent: [SkeletonElement] = [],
        extraSections: [SkeletonElement] = [],
        primaryButtons: [SkeletonElement],
        includeSessionThreadLiveReference: Bool = false
    ) -> CellConfiguration {
        var configuration = CellConfiguration(name: name)
        configuration.description = description
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: "cell:///ConferenceParticipantPreviewShell",
            sourceCellName: "ConferenceParticipantPreviewShellCell",
            purpose: name,
            purposeDescription: description,
            interests: ["conference", "participant", "agenda", "detail", "selection", "binding", "web"],
            menuSlots: ["upperMid", "lowerMid"]
        )

        var reference = CellReference(endpoint: "cell:///ConferenceParticipantPreviewShell", subscribeFeed: false, label: "conferenceParticipantShell")
        reference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        configuration.addReference(reference)

        if includeSessionThreadLiveReference {
            configuration.addReference(conferenceSessionThreadLiveReference())
        }

        var elements = SkeletonElementList()
        elements.append(catalogText(name))
        elements.append(
            catalogCardSection(
                "Detail",
                content: [
                    dashboardKeyText(titleKeypath),
                    dashboardKeyText(subtitleKeypath),
                    dashboardKeyText(detailKeypath),
                    dashboardKeyText(noteKeypath),
                    ] + extraContent + [
                    .HStack(SkeletonHStack(elements: primaryButtons))
                ]
            )
        )
        elements.append(contentsOf: extraSections)
        configuration.skeleton = .VStack(SkeletonVStack(elements: elements))
        return configuration
    }

    private static func sessionDetailComponentsSection(title: String) -> SkeletonElement {
        catalogCardSection(
            title,
            content: [
                dashboardKeyText("conferenceParticipantShell.state.sessionDetail.componentSummary"),
                .Grid(
                    SkeletonGrid(
                        columns: [.adaptive(min: 220, max: 320)],
                        spacing: 12,
                        keypath: "conferenceParticipantShell.state.sessionDetail.components",
                        itemSkeleton: conferenceParticipantPortalCardSkeleton()
                    )
                ),
                dashboardKeyText("conferenceParticipantShell.state.sessionDetail.slidesSummary"),
                dashboardKeyText("conferenceParticipantShell.state.sessionDetail.customComponentSummary"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "conferenceParticipantShell.state.sessionDetail.componentNotes",
                        flowElementSkeleton: conferenceParticipantPortalRowSkeleton(includeNote: true)
                    )
                )
            ]
        )
    }

    private static func compactConferenceChatSection(
        title: String,
        chatKeypathPrefix: String,
        primaryButtons: [SkeletonElement]
    ) -> SkeletonElement {
        catalogCardSection(
            title,
            content: [
                dashboardKeyText("\(chatKeypathPrefix).launchSummary"),
                dashboardKeyText("\(chatKeypathPrefix).conversationSummary"),
                dashboardKeyText("\(chatKeypathPrefix).messageSummary"),
                dashboardKeyText("\(chatKeypathPrefix).nextAction"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(chatKeypathPrefix).recentMessages",
                        flowElementSkeleton: dashboardMessageRowSkeleton()
                    )
                ),
                .HStack(SkeletonHStack(elements: primaryButtons))
            ]
        )
    }

    private static func sessionThreadLiveSection(
        title: String,
        primaryButtons: [SkeletonElement]
    ) -> SkeletonElement {
        catalogCardSection(
            title,
            content: [
                dashboardKeyText("conferenceSessionThread.state.sessionSummary"),
                dashboardKeyText("conferenceSessionThread.state.participationSummary"),
                dashboardKeyText("conferenceSessionThread.state.flowSummary"),
                dashboardKeyText("conferenceSessionThread.state.memberSummary"),
                dashboardKeyText("conferenceSessionThread.state.invitationSummary"),
                dashboardKeyText("conferenceSessionThread.state.lastActionSummary"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "conferenceSessionThread.state.messages",
                        flowElementSkeleton: dashboardMessageRowSkeleton()
                    )
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "conferenceSessionThread.state.members",
                        flowElementSkeleton: dashboardMessageRowSkeleton()
                    )
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "conferenceSessionThread.state.pendingInvitations",
                        flowElementSkeleton: dashboardMessageRowSkeleton()
                    )
                ),
                .TextArea(
                    SkeletonTextArea(
                        text: nil,
                        sourceKeypath: "conferenceSessionThread.state.editor.draft",
                        targetKeypath: "conferenceSessionThread.sessionThread.setDraft",
                        placeholder: "Skriv et spørsmål til denne sesjonen",
                        minLines: 3,
                        maxLines: 6
                    )
                ),
                .HStack(SkeletonHStack(elements: primaryButtons))
            ]
        )
    }

    private static func conferenceSessionThreadLiveReference() -> CellReference {
        var reference = CellReference(
            endpoint: "cell:///ConferenceSessionThreadLive",
            subscribeFeed: true,
            label: "conferenceSessionThread"
        )
        reference.setKeysAndValues = [KeyValue(key: "state", value: nil)]
        return reference
    }

    private static func loadConfigurationButton(
        _ label: String,
        configurationName: String,
        sourceCellEndpoint: String? = nil
    ) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 8
        modifiers.background = "#173140"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#2D566B"
        modifiers.foregroundColor = "#D9FBFF"
        modifiers.styleClasses = ["primary-action"]
        var lookup: Object = [
            "name": .string(configurationName)
        ]
        if let sourceCellEndpoint, sourceCellEndpoint.isEmpty == false {
            lookup["sourceCellEndpoint"] = .string(sourceCellEndpoint)
        }
        var button = SkeletonButton(
            keypath: "addConfiguration",
            label: label,
            payload: .object([
                "configurationLookup": .object(lookup)
            ])
        )
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func loadConcreteConfigurationButton(
        _ label: String,
        configuration: CellConfiguration
    ) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 8
        modifiers.background = "#173140"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#2D566B"
        modifiers.foregroundColor = "#D9FBFF"
        modifiers.styleClasses = ["primary-action"]
        var button = SkeletonButton(
            keypath: "addConfiguration",
            label: label,
            payload: .object([
                "configuration": .cellConfiguration(configuration)
            ])
        )
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func primaryActionButton(
        keypath: String,
        label: String,
        payload: ValueType = .bool(true)
    ) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 8
        modifiers.background = "#173140"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#2D566B"
        modifiers.foregroundColor = "#D9FBFF"
        modifiers.styleClasses = ["primary-action"]
        var button = SkeletonButton(
            keypath: keypath,
            label: label,
            payload: payload
        )
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func conferenceChatActionButton(label: String, text: String) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 8
        modifiers.background = "#173140"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#2D566B"
        modifiers.foregroundColor = "#D9FBFF"
        modifiers.styleClasses = ["primary-action"]
        var button = SkeletonButton(
            keypath: "conferenceChat.sendMessage",
            label: label,
            payload: .object(["text": .string(text)])
        )
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func participantPortalActionButton(
        _ referenceLabel: String,
        actionKeypath: String,
        label: String,
        payload: ValueType = .bool(true)
    ) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 8
        modifiers.background = "#173140"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#2D566B"
        modifiers.foregroundColor = "#D9FBFF"
        modifiers.styleClasses = ["primary-action"]
        var button = SkeletonButton(
            keypath: "\(referenceLabel).dispatchAction",
            label: label,
            payload: .object([
                "keypath": .string(actionKeypath),
                "payload": payload
            ])
        )
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func participantPortalDirectActionButton(
        keypath: String,
        label: String,
        payload: ValueType? = nil
    ) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 8
        modifiers.background = "#173140"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#2D566B"
        modifiers.foregroundColor = "#D9FBFF"
        modifiers.styleClasses = ["primary-action"]
        var button = SkeletonButton(
            keypath: keypath,
            label: label,
            payload: payload
        )
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func participantPortalNetworkSection(referenceLabel: String) -> SkeletonElement {
        catalogCardSection(
            "Nettverks-Hub",
            content: [
                dashboardKeyText("\(referenceLabel).state.sharedConnections.intro"),
                dashboardKeyText("\(referenceLabel).state.sharedConnections.accessSummary"),
                dashboardKeyText("\(referenceLabel).state.sharedConnections.connectionSummary"),
                dashboardKeyText("\(referenceLabel).state.sharedConnections.chatSummary"),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.sharedConnections.connections",
                        flowElementSkeleton: dashboardConnectionRowSkeleton()
                    )
                ),
                .List(
                    SkeletonList(
                        topic: nil,
                        keypath: "\(referenceLabel).state.sharedConnections.recentMessages",
                        flowElementSkeleton: dashboardMessageRowSkeleton()
                    )
                ),
                .HStack(
                    SkeletonHStack(elements: [
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "connections.postSharedMessage",
                            label: "Send oppfølging",
                            payload: .object([
                                "text": .string("Takk for praten. Skal vi fortsette etter neste sesjon?"),
                                "contentType": .string("text/plain")
                            ])
                        ),
                        participantPortalActionButton(
                            referenceLabel,
                            actionKeypath: "scheduling.respondMeetingRequest",
                            label: "Vurder forespørsel"
                        )
                    ])
                )
            ]
        )
    }

    private static func dashboardStaticText(
        _ text: String,
        fontSize: Double? = nil,
        fontWeight: String? = nil,
        foregroundColor: String? = nil
    ) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.fontSize = fontSize
        modifiers.fontWeight = fontWeight
        modifiers.foregroundColor = foregroundColor ?? "#D5E4ED"
        var element = SkeletonText(text: text)
        element.modifiers = modifiers
        return .Text(element)
    }

    private static func dashboardKeyText(
        _ keypath: String,
        fontSize: Double? = nil,
        fontWeight: String? = nil,
        foregroundColor: String? = nil
    ) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.fontSize = fontSize
        modifiers.fontWeight = fontWeight
        modifiers.foregroundColor = foregroundColor ?? "#D5E4ED"
        var element = SkeletonText(keypath: keypath)
        element.modifiers = modifiers
        return .Text(element)
    }

    private static func selectableDashboardList(
        keypath: String,
        selectionStateKeypath: String,
        selectionActionKeypath: String,
        rowSkeleton: SkeletonVStack,
        styleClasses: [String] = []
    ) -> SkeletonElement {
        var list = SkeletonList(
            topic: nil,
            keypath: keypath,
            flowElementSkeleton: rowSkeleton
        )
        list.selectionMode = .single
        list.selectionValueKeypath = "id"
        list.selectionStateKeypath = selectionStateKeypath
        list.selectionActionKeypath = selectionActionKeypath
        list.activationActionKeypath = selectionActionKeypath
        list.selectionPayloadMode = .itemID
        list.allowsEmptySelection = false
        if styleClasses.isEmpty == false {
            var modifiers = SkeletonModifiers()
            modifiers.styleClasses = styleClasses
            list.modifiers = modifiers
        }
        return .List(list)
    }

    private static func multiSelectableDashboardList(
        keypath: String,
        selectionStateKeypath: String,
        selectionActionKeypath: String,
        rowSkeleton: SkeletonVStack,
        styleClasses: [String] = [],
        allowsEmptySelection: Bool
    ) -> SkeletonElement {
        var list = SkeletonList(
            topic: nil,
            keypath: keypath,
            flowElementSkeleton: rowSkeleton
        )
        list.selectionMode = .multiple
        list.selectionValueKeypath = "id"
        list.selectionStateKeypath = selectionStateKeypath
        list.selectionActionKeypath = selectionActionKeypath
        list.selectionPayloadMode = .selectedIDs
        list.allowsEmptySelection = allowsEmptySelection
        if styleClasses.isEmpty == false {
            var modifiers = SkeletonModifiers()
            modifiers.styleClasses = styleClasses
            list.modifiers = modifiers
        }
        return .List(list)
    }

    private static func styledDashboardList(
        keypath: String,
        rowSkeleton: SkeletonVStack,
        styleClasses: [String]
    ) -> SkeletonList {
        var list = SkeletonList(
            topic: nil,
            keypath: keypath,
            flowElementSkeleton: rowSkeleton
        )
        var modifiers = SkeletonModifiers()
        modifiers.styleClasses = styleClasses
        list.modifiers = modifiers
        return list
    }

    private static func dashboardBadgeKeyText(_ keypath: String) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 6
        modifiers.background = "#122734"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#244457"
        modifiers.foregroundColor = "#C6F5EE"
        modifiers.fontSize = 12
        modifiers.fontWeight = "semibold"
        modifiers.styleClasses = ["conference-badge"]
        var element = SkeletonText(keypath: keypath)
        element.modifiers = modifiers
        return .Text(element)
    }

    private static func dashboardRecommendationRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardBadgeKeyText("note"),
            .Divider(SkeletonDivider())
        ])
    }

    private static func dashboardRecommendationCardSkeleton() -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.background = "#122734"
        modifiers.cornerRadius = 12
        modifiers.borderWidth = 1
        modifiers.borderColor = "#244457"

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardBadgeKeyText("note"),
            .HStack(SkeletonHStack(elements: [
                participantPortalRowActionButton(),
                participantPortalRowMeetingButton()
            ]))
        ])
        section.modifiers = modifiers
        return .Section(section)
    }

    private static func dashboardMetricCardSkeleton() -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.background = "#122734"
        modifiers.cornerRadius = 12
        modifiers.borderWidth = 1
        modifiers.borderColor = "#244457"

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardBadgeKeyText("note")
        ])
        section.modifiers = modifiers
        return .Section(section)
    }

    private static func dashboardTimelineRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            .Divider(SkeletonDivider())
        ])
    }

    private static func dashboardInteractiveTimelineRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            participantPortalRowActionButton(),
            .Divider(SkeletonDivider())
        ])
    }

    private static func dashboardAgendaTrackCardRowSkeleton() -> SkeletonVStack {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.background = "#0F1B24"
        modifiers.cornerRadius = 12
        modifiers.borderWidth = 1
        modifiers.borderColor = "#1F3442"
        modifiers.styleClasses = ["conference-agenda-track-card"]

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            .HStack(SkeletonHStack(elements: [
                participantPortalRowActionButton(),
                participantPortalDetailRowButton()
            ]))
        ])
        section.modifiers = modifiers
        return SkeletonVStack(elements: [.Section(section)])
    }

    private static func dashboardAgendaSessionCardRowSkeleton(recommended: Bool) -> SkeletonVStack {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.background = recommended ? "#2B2413" : "#122734"
        modifiers.cornerRadius = 12
        modifiers.borderWidth = 1
        modifiers.borderColor = recommended ? "#D7B24A" : "#244457"
        modifiers.styleClasses = recommended
            ? ["conference-agenda-session-card", "conference-agenda-session-card--recommended"]
            : ["conference-agenda-session-card"]

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            participantPortalRowActionButton()
        ])
        section.modifiers = modifiers
        return SkeletonVStack(elements: [.Section(section)])
    }

    private static func dashboardAgendaTimeSlotMatrixRowSkeleton(referenceLabel: String) -> SkeletonVStack {
        var rowModifiers = SkeletonModifiers()
        rowModifiers.padding = 14
        rowModifiers.background = "#101C25"
        rowModifiers.cornerRadius = 14
        rowModifiers.borderWidth = 1
        rowModifiers.borderColor = "#2A4A5F"
        rowModifiers.styleClasses = ["conference-agenda-timeslot-row"]

        var trackGridModifiers = SkeletonModifiers()
        trackGridModifiers.styleClasses = ["conference-agenda-timeslot-grid", "conference-agenda-timeslot-track-grid"]

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#A9C4D4"),
            .Grid(
                SkeletonGrid(
                    columns: [.adaptive(min: 220, max: 320)],
                    spacing: 12,
                    keypath: "trackCells",
                    itemSkeleton: dashboardAgendaTimeSlotTrackCellSkeleton(referenceLabel: referenceLabel),
                    modifiers: trackGridModifiers
                )
            )
        ])
        section.modifiers = rowModifiers
        return SkeletonVStack(elements: [.Section(section)])
    }

    private static func dashboardAgendaTimeSlotTrackCellSkeleton(referenceLabel: String) -> SkeletonElement {
        var cellModifiers = SkeletonModifiers()
        cellModifiers.padding = 12
        cellModifiers.background = "#0F1B24"
        cellModifiers.cornerRadius = 12
        cellModifiers.borderWidth = 1
        cellModifiers.borderColor = "#1F3442"
        cellModifiers.styleClasses = ["conference-agenda-track-cell"]

        var recommendedList = SkeletonList(
            topic: nil,
            keypath: "recommendedSessions",
            flowElementSkeleton: dashboardAgendaSessionCardRowSkeleton(recommended: true)
        )
        recommendedList.selectionMode = .single
        recommendedList.selectionValueKeypath = "id"
        recommendedList.selectionStateKeypath = "\(referenceLabel).state.program.selectedSessionID"
        recommendedList.selectionActionKeypath = "\(referenceLabel).agenda.selectSession"
        recommendedList.selectionPayloadMode = .itemID
        recommendedList.allowsEmptySelection = false
        var recommendedModifiers = SkeletonModifiers()
        recommendedModifiers.styleClasses = ["conference-agenda-session-list", "conference-agenda-card-list", "conference-agenda-recommended-list", "conference-agenda-track-cell-list"]
        recommendedList.modifiers = recommendedModifiers

        var regularList = SkeletonList(
            topic: nil,
            keypath: "sessions",
            flowElementSkeleton: dashboardAgendaSessionCardRowSkeleton(recommended: false)
        )
        regularList.selectionMode = .single
        regularList.selectionValueKeypath = "id"
        regularList.selectionStateKeypath = "\(referenceLabel).state.program.selectedSessionID"
        regularList.selectionActionKeypath = "\(referenceLabel).agenda.selectSession"
        regularList.selectionPayloadMode = .itemID
        regularList.allowsEmptySelection = false
        var regularModifiers = SkeletonModifiers()
        regularModifiers.styleClasses = ["conference-agenda-session-list", "conference-agenda-card-list", "conference-agenda-track-cell-list"]
        regularList.modifiers = regularModifiers

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#A9C4D4"),
            .List(recommendedList),
            .List(regularList)
        ])
        section.modifiers = cellModifiers
        return .Section(section)
    }

    private static func dashboardAgendaTrackGroupRowSkeleton(referenceLabel: String) -> SkeletonVStack {
        var groupModifiers = SkeletonModifiers()
        groupModifiers.padding = 14
        groupModifiers.background = "#101E29"
        groupModifiers.cornerRadius = 14
        groupModifiers.borderWidth = 1
        groupModifiers.borderColor = "#214055"
        groupModifiers.styleClasses = ["conference-agenda-track-group"]

        var recommendedList = SkeletonList(
            topic: nil,
            keypath: "recommendedSessions",
            flowElementSkeleton: dashboardAgendaSessionCardRowSkeleton(recommended: true)
        )
        recommendedList.selectionMode = .single
        recommendedList.selectionValueKeypath = "id"
        recommendedList.selectionStateKeypath = "\(referenceLabel).state.program.selectedSessionID"
        recommendedList.selectionActionKeypath = "\(referenceLabel).agenda.selectSession"
        recommendedList.selectionPayloadMode = .itemID
        recommendedList.allowsEmptySelection = false
        var recommendedModifiers = SkeletonModifiers()
        recommendedModifiers.styleClasses = ["conference-agenda-session-list", "conference-agenda-card-list", "conference-agenda-recommended-list"]
        recommendedList.modifiers = recommendedModifiers

        var regularList = SkeletonList(
            topic: nil,
            keypath: "sessions",
            flowElementSkeleton: dashboardAgendaSessionCardRowSkeleton(recommended: false)
        )
        regularList.selectionMode = .single
        regularList.selectionValueKeypath = "id"
        regularList.selectionStateKeypath = "\(referenceLabel).state.program.selectedSessionID"
        regularList.selectionActionKeypath = "\(referenceLabel).agenda.selectSession"
        regularList.selectionPayloadMode = .itemID
        regularList.allowsEmptySelection = false
        var regularModifiers = SkeletonModifiers()
        regularModifiers.styleClasses = ["conference-agenda-session-list", "conference-agenda-card-list"]
        regularList.modifiers = regularModifiers

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 16, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("sessionSummary", fontSize: 12, foregroundColor: "#A9C4D4"),
            .List(recommendedList),
            .List(regularList)
        ])
        section.modifiers = groupModifiers
        return SkeletonVStack(elements: [.Section(section)])
    }

    private static func dashboardSessionCardSkeleton() -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.background = "#122734"
        modifiers.cornerRadius = 12
        modifiers.borderWidth = 1
        modifiers.borderColor = "#244457"

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            participantPortalRowActionButton()
        ])
        section.modifiers = modifiers
        return .Section(section)
    }

    private static func dashboardTrackCardSkeleton() -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.background = "#0F1B24"
        modifiers.cornerRadius = 12
        modifiers.borderWidth = 1
        modifiers.borderColor = "#1F3442"

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            participantPortalRowActionButton()
        ])
        section.modifiers = modifiers
        return .Section(section)
    }

    private static func dashboardConnectionRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            .Divider(SkeletonDivider())
        ])
    }

    private static func dashboardDiscoveryRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            participantPortalRowActionButton(),
            .Divider(SkeletonDivider())
        ])
    }

    private static func dashboardDiscoveryCardSkeleton() -> SkeletonVStack {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.background = "#122734"
        modifiers.cornerRadius = 12
        modifiers.borderWidth = 1
        modifiers.borderColor = "#244457"
        modifiers.styleClasses = ["conference-agenda-session-card", "conference-discovery-card"]

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            participantPortalRowActionButton()
        ])
        section.modifiers = modifiers
        return SkeletonVStack(elements: [.Section(section)])
    }

    private static func dashboardProofDiscoveryCardSkeleton() -> SkeletonVStack {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 12
        modifiers.background = "#173126"
        modifiers.cornerRadius = 12
        modifiers.borderWidth = 1
        modifiers.borderColor = "#2B5B46"
        modifiers.styleClasses = ["conference-agenda-session-card", "conference-discovery-card", "conference-proof-card"]

        var section = SkeletonSection(content: [
            dashboardKeyText("title", fontSize: 15, fontWeight: "bold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("subtitle", fontSize: 12, foregroundColor: "#8DE1DA"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            participantPortalRowActionButton()
        ])
        section.modifiers = modifiers
        return SkeletonVStack(elements: [.Section(section)])
    }

    private static func dashboardMessageRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            dashboardKeyText("title", fontSize: 14, fontWeight: "semibold", foregroundColor: "#F5FBFF"),
            dashboardKeyText("detail", fontSize: 12, foregroundColor: "#D5E4ED"),
            dashboardKeyText("note", fontSize: 12, foregroundColor: "#D5E4ED"),
            .Divider(SkeletonDivider())
        ])
    }

    private static func participantPortalRowActionButton() -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 8
        modifiers.background = "#173140"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#2D566B"
        modifiers.foregroundColor = "#D9FBFF"
        modifiers.styleClasses = ["primary-action"]
        var button = SkeletonButton(keypath: "conferenceParticipantShell.dispatchAction", label: "Action")
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func participantPortalRowMeetingButton() -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 8
        modifiers.background = "#173140"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#2D566B"
        modifiers.foregroundColor = "#D9FBFF"
        modifiers.styleClasses = ["primary-action", "secondary-action"]
        var button = SkeletonButton(
            keypath: "conferenceParticipantShell.dispatchAction",
            label: "Be om møte",
            labelKeypath: "meetingLabel",
            payloadKeypath: "meetingPayload"
        )
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func participantPortalDetailRowButton() -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 8
        modifiers.background = "#173140"
        modifiers.cornerRadius = 8
        modifiers.borderWidth = 1
        modifiers.borderColor = "#2D566B"
        modifiers.foregroundColor = "#D9FBFF"
        modifiers.styleClasses = ["primary-action"]
        var button = SkeletonButton(
            keypath: "addConfiguration",
            label: "Åpne detaljer",
            keypathKeypath: "detailKeypath",
            labelKeypath: "detailLabel",
            payloadKeypath: "detailPayload"
        )
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func mermaidWebViewSVGPayload(source: String, correlationId: String) -> Object {
        [
            "source": .string(source),
            "config": .object([
                "backend": .string("webview"),
                "output": .string("svgText"),
                "theme": .string("default"),
                "engineVersion": .string(MermaidRenderConfig.defaultWebViewEngineVersion),
                "deterministicMode": .bool(true)
            ]),
            "cachePolicy": .string("useCache"),
            "correlationId": .string(correlationId)
        ]
    }

    private static func conferenceOwnershipDiagramRenderPayload(backend: MarkdownRenderBackend) -> Object {
        [
            "doc_id": .string(conferenceOwnershipDocID),
            "backend": .string(backend.rawValue),
            "resolve_links": .bool(true),
            "render_mermaid": .bool(true),
            "include_table_of_contents": .bool(true)
        ]
    }

    private static func mermaidWebViewPNGPayload(source: String, correlationId: String) -> Object {
        [
            "source": .string(source),
            "config": .object([
                "backend": .string("webview"),
                "output": .string("pngBytes"),
                "theme": .string("default"),
                "width": .integer(960),
                "height": .integer(640),
                "scale": .float(1.0),
                "engineVersion": .string(MermaidRenderConfig.defaultWebViewEngineVersion),
                "deterministicMode": .bool(true)
            ]),
            "cachePolicy": .string("useCache"),
            "correlationId": .string(correlationId)
        ]
    }

    private static func mermaidNativePNGPayload(source: String, correlationId: String) -> Object {
        let nativeEngineVersion = MermaidNativeRenderer().engineVersion
        return [
            "source": .string(source),
            "config": .object([
                "backend": .string("native"),
                "output": .string("pngBytes"),
                "theme": .string("default"),
                "width": .integer(960),
                "height": .integer(640),
                "scale": .float(1.0),
                "engineVersion": .string(nativeEngineVersion),
                "deterministicMode": .bool(true)
            ]),
            "cachePolicy": .string("useCache"),
            "correlationId": .string(correlationId)
        ]
    }

    private static func vaultCreateNotePayload(id: String, title: String, content: String, tags: [String]) -> Object {
        [
            "id": .string(id),
            "title": .string(title),
            "content": .string(content),
            "tags": .list(tags.map(ValueType.string))
        ]
    }

    private static func vaultUpdateNotePayload(id: String, title: String, content: String, tags: [String]) -> Object {
        vaultCreateNotePayload(id: id, title: title, content: content, tags: tags)
    }

    private static func vaultGetNotePayload(id: String) -> Object {
        ["id": .string(id)]
    }

    private static func vaultListNotesPayload(tags: [String], limit: Int) -> Object {
        [
            "tags": .list(tags.map(ValueType.string)),
            "limit": .integer(limit),
            "sortBy": .string("updatedAt"),
            "descending": .bool(true)
        ]
    }

    private static func vaultAddLinkPayload(fromNoteID: String, toNoteID: String) -> Object {
        [
            "fromNoteID": .string(fromNoteID),
            "toNoteID": .string(toNoteID),
            "relationship": .string("wiki")
        ]
    }

    private static func singleReferenceConfiguration(
        name: String,
        endpoint: String,
        label: String,
        sourceCellName: String,
        purpose: String,
        purposeDescription: String,
        interests: [String],
        menuSlots: [MenuSlot]
    ) -> CellConfiguration {
        var configuration = CellConfiguration(name: name)
        configuration.description = purposeDescription
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: endpoint,
            sourceCellName: sourceCellName,
            purpose: purpose,
            purposeDescription: purposeDescription,
            interests: interests,
            menuSlots: menuSlots.map(\.rawValue)
        )
        let reference = CellReference(endpoint: endpoint, label: label)
        configuration.addReference(reference)
        return configuration
    }

    static func adminDashboardConfiguration(
        adminRouting: AdminControlPlaneRouting = .current
    ) -> CellConfiguration {
        AdminDashboardConfigurationFactory.make(adminRouting: adminRouting)
    }

    private static func adminProcessRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            .Text(SkeletonText(keypath: "command")),
            .Text(SkeletonText(keypath: "cpuPercent")),
            .Text(SkeletonText(keypath: "mem")),
            .Text(SkeletonText(keypath: "threads")),
            .Text(SkeletonText(keypath: "time")),
            .Divider(SkeletonDivider())
        ])
    }

    private static func adminStorageRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            .Text(SkeletonText(keypath: "uuid")),
            .Text(SkeletonText(keypath: "directoryBytes")),
            .Text(SkeletonText(keypath: "typedCellBytes")),
            .Divider(SkeletonDivider())
        ])
    }

    private static func adminIssuerRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            .Text(SkeletonText(keypath: "did")),
            .Text(SkeletonText(keypath: "label")),
            .Text(SkeletonText(keypath: "addedAt")),
            .Divider(SkeletonDivider())
        ])
    }

    private static func adminFundingResourceRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            .Text(SkeletonText(keypath: "resourceID")),
            .Text(SkeletonText(keypath: "priceMinorUnits")),
            .Divider(SkeletonDivider())
        ])
    }

    private static func adminFundingRequestRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            .Text(SkeletonText(keypath: "id")),
            .Text(SkeletonText(keypath: "username")),
            .Text(SkeletonText(keypath: "status")),
            .Text(SkeletonText(keypath: "requestedMinorUnits")),
            .Text(SkeletonText(keypath: "riskFlags")),
            .Divider(SkeletonDivider())
        ])
    }

    private static func adminFundingAuditRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            .Text(SkeletonText(keypath: "action")),
            .Text(SkeletonText(keypath: "actorUserID")),
            .Text(SkeletonText(keypath: "targetRequestID")),
            .Text(SkeletonText(keypath: "createdAt")),
            .Divider(SkeletonDivider())
        ])
    }

    private static func todoPlannerItemRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            .Text(SkeletonText(keypath: "title")),
            .Text(SkeletonText(keypath: "dueText")),
            .Text(SkeletonText(keypath: "recurrenceText")),
            .Text(SkeletonText(keypath: "priorityText")),
            .Text(SkeletonText(keypath: "importantText")),
            .Text(SkeletonText(keypath: "labelsText")),
            .Text(SkeletonText(keypath: "stepProgressText")),
            .Text(SkeletonText(keypath: "statusText")),
            .Divider(SkeletonDivider())
        ])
    }

    private static func ideaTaskIdeaRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            .Text(SkeletonText(keypath: "title")),
            .Text(SkeletonText(keypath: "stageLabel")),
            .Text(SkeletonText(keypath: "tagsText")),
            .Text(SkeletonText(keypath: "contentPreview")),
            .Text(SkeletonText(keypath: "relatedTodoCount")),
            .Divider(SkeletonDivider())
        ])
    }

    private static func ideaTaskActionButton(
        keypath: String,
        label: String,
        payload: ValueType = .object([:]),
        emphasis: Bool = false
    ) -> SkeletonElement {
        var button = SkeletonButton(keypath: keypath, label: label, payload: payload)
        var modifiers = SkeletonModifiers()
        modifiers.padding = 8
        modifiers.cornerRadius = 10
        modifiers.background = emphasis ? "#1F5C68" : "#132A35"
        modifiers.borderWidth = 1
        modifiers.borderColor = emphasis ? "#7FD6D0" : "#234454"
        modifiers.foregroundColor = "#F5FBFF"
        modifiers.styleClasses = emphasis ? ["idea-action", "primary-action"] : ["idea-action"]
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func ideaTaskTodoRowSkeleton() -> SkeletonVStack {
        SkeletonVStack(elements: [
            .Text(SkeletonText(keypath: "title")),
            .Text(SkeletonText(keypath: "dueText")),
            .Text(SkeletonText(keypath: "priorityText")),
            .Text(SkeletonText(keypath: "importantText")),
            .Text(SkeletonText(keypath: "labelsText")),
            .Text(SkeletonText(keypath: "stepProgressText")),
            .Text(SkeletonText(keypath: "statusText")),
            .Divider(SkeletonDivider())
        ])
    }

    private func emitCatalogEvent(operation: String, entry: CatalogEntry?, requester: Identity) async {
        var payload: Object = ["operation": .string(operation), "state": stateValue()]
        if let entry {
            payload["entry"] = .object(entry.asObject())
        }

        var flowElement = FlowElement(
            title: "configuration.catalog.\(operation)",
            content: .object(payload),
            properties: FlowElement.Properties(type: .event, contentType: .object)
        )
        flowElement.topic = "configurationCatalog"
        flowElement.origin = uuid

        if let owner = try? await getOwner(requester: requester) {
            pushFlowElement(flowElement, requester: owner)
        } else {
            pushFlowElement(flowElement, requester: requester)
        }
    }
}
