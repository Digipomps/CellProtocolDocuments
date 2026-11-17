// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

import Foundation
import Vapor
import CellBase
import CellVapor
import ScaffoldKit

struct PortholeActionRequest: Content, Codable {
    let keypath: String?
    let payload: ValueType?
    let command: String?
    let args: ValueType?

    var resolvedKeypath: String? {
        let raw = (keypath ?? command ?? "").trimmingCharacters(in: .whitespacesAndNewlines)
        return raw.isEmpty ? nil : raw
    }

    var resolvedPayload: ValueType? {
        payload ?? args
    }
}

struct PortholeWebSocketServerEnvelope: Codable {
    let kind: String
    let requestId: String?
    let payload: ValueType?
    let message: String?
    let ok: Bool?
}

struct PortholeLoadedReferenceReadiness: Equatable {
    let readyLabels: [String]
    let accessGatedLabels: [String: String]
    let unavailableLabels: [String]
    let unresolvedLabels: [String]
}

enum PortholeConferencePersonaSelection: Equatable {
    case inheritStored
    case clearStored
    case persona(String)
}

enum PortholeWebSessionSupport {
    static let conferencePersonaQueryKey = "conferencePersona"
    static let conferencePersonaSessionKey = "portholeConferencePersona"
    static let conferencePersonaWarningSessionKey = "portholeConferencePersonaWarning"
    static let conferencePersonaStableIdentityDomain = "conference-demo-personas"
    static let conferencePersonaDevelopmentOptInEnvironmentKey = "CONFERENCE_DEMO_PERSONAS_ENABLED"
    static let configurationNameQueryKey = "configurationName"
    static let configurationEndpointQueryKey = "configurationEndpoint"
    static let configurationUUIDQueryKey = "configurationUUID"
    static let surfaceIDQueryKey = "surfaceID"
    static let showProductChromeQueryKey = "showProductChrome"
    private static let accessRequirementPromptEndpoint = "cell:///AccessRequirementPrompt"
    private static let accessRequirementPromptReferenceName = "AccessRequirementPrompt"
    private static let accessRequirementDecisionStore = AccessRequirementDecisionStore()
    nonisolated(unsafe) private static var configuredScaffoldUtilityRequester: Identity?

    static func configureScaffoldUtilityRequester(_ requester: Identity?) {
        configuredScaffoldUtilityRequester = requester
    }

    struct ConferencePersonaRequest: Equatable {
        let selection: PortholeConferencePersonaSelection
        let warning: String?
    }

    private struct BootstrapAccessRequirement {
        let kind: String
        let referenceLabel: String
        let sourceCellEndpoint: String
        let requestedKeypaths: [String]
        let denialReason: String
        let subjectLabel: String
        let grantKeypath: String
        let grantPermission: String
        let agreementName: String
        let purpose: String
        let durationHours: Int
        let proofKeypath: String?
        let proofCredentialType: String?
        let proofPrompt: String?
        let admissionMode: String
        let resolutionHint: String?
        let resolutionRequesterUUID: String?
        let resolutionRequesterDisplayName: String?

        var externalApprovalRequired: Bool {
            admissionMode == "admin_external_authorization"
        }

        var paymentResolutionRequired: Bool {
            admissionMode == "payment_required"
        }

        var fingerprint: String {
            let discriminator = kind == "prove" ? (proofKeypath ?? grantKeypath) : grantKeypath
            return "\(kind)|\(sourceCellEndpoint)|\(discriminator)|\(subjectLabel)"
        }

        var value: ValueType {
            .object([
                "kind": .string(kind),
                "fingerprint": .string(fingerprint),
                "referenceLabel": .string(referenceLabel),
                "sourceCellEndpoint": .string(sourceCellEndpoint),
                "requestedKeypaths": .list(requestedKeypaths.map(ValueType.string)),
                "denialReason": .string(denialReason),
                "subjectLabel": .string(subjectLabel),
                "targetEndpoint": .string(sourceCellEndpoint),
                "grantKeypath": .string(grantKeypath),
                "grantPermission": .string(grantPermission),
                "agreementName": .string(agreementName),
                "purpose": .string(purpose),
                "durationHours": .integer(durationHours),
                "proofKeypath": proofKeypath.map(ValueType.string) ?? .null,
                "proofCredentialType": proofCredentialType.map(ValueType.string) ?? .null,
                "proofPrompt": proofPrompt.map(ValueType.string) ?? .null,
                "admissionMode": .string(admissionMode),
                "externalApprovalRequired": .bool(externalApprovalRequired),
                "paymentResolutionRequired": .bool(paymentResolutionRequired),
                "resolutionHint": resolutionHint.map(ValueType.string) ?? .null,
                "resolutionRequesterUUID": resolutionRequesterUUID.map(ValueType.string) ?? .null,
                "resolutionRequesterDisplayName": resolutionRequesterDisplayName.map(ValueType.string) ?? .null
            ])
        }
    }

    private struct InferredRequirementDetails {
        let kind: String
        let grantKeypath: String
        let grantPermission: String
        let proofKeypath: String?
        let proofCredentialType: String?
        let proofPrompt: String?
    }

    private struct PublishedAccessRequirementContract {
        let kind: String
        let subjectLabel: String?
        let grantKeypath: String
        let grantPermission: String
        let agreementName: String?
        let purpose: String?
        let durationHours: Int?
        let proofKeypath: String?
        let proofCredentialType: String?
        let proofPrompt: String?
        let requestedKeypaths: [String]
    }

    private struct NestedRequirementDescriptor {
        let nestedStateKeypath: String
        let labelSuffix: String
        let endpoint: String
        let denialReason: String
        let resolutionHint: String?
        let resolutionRequesterUUID: String?
        let resolutionRequesterDisplayName: String?
    }

    enum BootstrapReadResult {
        case value(ValueType)
        case accessDenied(String)
        case unavailable
    }

    private actor AccessRequirementDecisionStore {
        private var dismissedFingerprintsBySession = [String: Set<String>]()
        private var activeFingerprintBySession = [String: String]()

        func setActiveFingerprint(_ fingerprint: String?, sessionId: String) {
            guard sessionId.isEmpty == false else { return }
            guard let fingerprint, fingerprint.isEmpty == false else {
                activeFingerprintBySession[sessionId] = nil
                return
            }
            activeFingerprintBySession[sessionId] = fingerprint
        }

        func activeFingerprint(sessionId: String) -> String? {
            activeFingerprintBySession[sessionId]
        }

        func dismiss(_ fingerprint: String, sessionId: String) {
            guard fingerprint.isEmpty == false, sessionId.isEmpty == false else { return }
            dismissedFingerprintsBySession[sessionId, default: []].insert(fingerprint)
        }

        func clearDismissal(_ fingerprint: String, sessionId: String) {
            guard fingerprint.isEmpty == false, sessionId.isEmpty == false else { return }
            dismissedFingerprintsBySession[sessionId]?.remove(fingerprint)
            if dismissedFingerprintsBySession[sessionId]?.isEmpty == true {
                dismissedFingerprintsBySession[sessionId] = nil
            }
        }

        func isDismissed(_ fingerprint: String, sessionId: String) -> Bool {
            dismissedFingerprintsBySession[sessionId]?.contains(fingerprint) == true
        }
    }

    private actor RuntimeBindingBootstrapStore {
        private final class WeakTarget {
            weak var target: AnyObject?

            init(_ target: AnyObject) {
                self.target = target
            }
        }

        private struct Key: Hashable {
            let targetID: ObjectIdentifier
            let requesterKey: String
        }

        private var targetsByID = [ObjectIdentifier: WeakTarget]()
        private var completed = Set<Key>()
        private var waiters = [Key: [CheckedContinuation<Void, Never>]]()

        func begin(_ target: AnyObject, requester: Identity) async -> Bool {
            pruneReleasedTargets()
            let targetID = ObjectIdentifier(target)
            targetsByID[targetID] = WeakTarget(target)
            let key = Key(
                targetID: targetID,
                requesterKey: PortholeRuntimeBindingIdentityKey.ownerKey(for: requester)
            )
            if completed.contains(key) {
                return false
            }
            if waiters[key] != nil {
                await withCheckedContinuation { continuation in
                    waiters[key, default: []].append(continuation)
                }
                return false
            }
            waiters[key] = []
            return true
        }

        func finish(_ target: AnyObject, requester: Identity) {
            let key = Key(
                targetID: ObjectIdentifier(target),
                requesterKey: PortholeRuntimeBindingIdentityKey.ownerKey(for: requester)
            )
            completed.insert(key)
            let continuations = waiters.removeValue(forKey: key) ?? []
            for continuation in continuations {
                continuation.resume()
            }
        }

        func abort(_ target: AnyObject, requester: Identity) {
            let key = Key(
                targetID: ObjectIdentifier(target),
                requesterKey: PortholeRuntimeBindingIdentityKey.ownerKey(for: requester)
            )
            let continuations = waiters.removeValue(forKey: key) ?? []
            for continuation in continuations {
                continuation.resume()
            }
        }

        private func pruneReleasedTargets() {
            let releasedIDs = Set(targetsByID.compactMap { targetID, weakTarget in
                weakTarget.target == nil ? targetID : nil
            })
            guard releasedIDs.isEmpty == false else { return }
            targetsByID = targetsByID.filter { releasedIDs.contains($0.key) == false }
            completed = completed.filter { releasedIDs.contains($0.targetID) == false }
            waiters = waiters.filter { releasedIDs.contains($0.key.targetID) == false }
        }
    }

    private static let runtimeBindingBootstrapStore = RuntimeBindingBootstrapStore()

    static func requestedConferencePersonaRequest(in req: Request) -> ConferencePersonaRequest {
        guard requestContainsConferencePersonaQuery(in: req) else {
            return ConferencePersonaRequest(selection: .inheritStored, warning: nil)
        }

        guard conferencePersonasEnabled(in: req) else {
            return ConferencePersonaRequest(
                selection: .clearStored,
                warning: "Conference demo-personaer er deaktivert. Fortsetter som innlogget requester; organizer-tilgang krever owner-proof eller gyldig credential."
            )
        }

        let queryValue: String? = req.query[String.self, at: conferencePersonaQueryKey]
        let rawValue = queryValue?.trimmingCharacters(in: .whitespacesAndNewlines)

        guard let rawValue, rawValue.isEmpty == false else {
            return ConferencePersonaRequest(selection: .clearStored, warning: nil)
        }

        do {
            _ = try ConferencePlaywrightPersonaBootstrap.persona(id: rawValue)
            return ConferencePersonaRequest(selection: .persona(rawValue), warning: nil)
        } catch {
            return ConferencePersonaRequest(
                selection: .clearStored,
                warning: "Conference demo-persona '\(rawValue)' er ikke tilgjengelig i denne deployen. Fortsetter som innlogget requester."
            )
        }
    }

    static func requestedConferencePersonaSelection(in req: Request) throws -> PortholeConferencePersonaSelection {
        guard requestContainsConferencePersonaQuery(in: req) else {
            return .inheritStored
        }
        guard conferencePersonasEnabled(in: req) else {
            return .clearStored
        }

        let queryValue: String? = req.query[String.self, at: conferencePersonaQueryKey]
        let rawValue = queryValue?.trimmingCharacters(in: .whitespacesAndNewlines)

        guard let rawValue, rawValue.isEmpty == false else {
            return .clearStored
        }

        _ = try ConferencePlaywrightPersonaBootstrap.persona(id: rawValue)
        return .persona(rawValue)
    }

    static func storedConferencePersonaID(in req: Request) -> String? {
        guard conferencePersonasEnabled(in: req) else {
            req.session.data[conferencePersonaSessionKey] = nil
            return nil
        }
        guard let storedValue = req.session.data[conferencePersonaSessionKey]?
            .trimmingCharacters(in: .whitespacesAndNewlines),
              storedValue.isEmpty == false else {
            return nil
        }
        return storedValue
    }

    static func storedConferencePersonaWarning(in req: Request) -> String? {
        guard let storedValue = req.session.data[conferencePersonaWarningSessionKey]?
            .trimmingCharacters(in: .whitespacesAndNewlines),
              storedValue.isEmpty == false else {
            return nil
        }
        return storedValue
    }

    static func requestedConfigurationPayload(in req: Request) -> ValueType? {
        let surfaceID = req.query[String.self, at: surfaceIDQueryKey]?
            .trimmingCharacters(in: .whitespacesAndNewlines)
        let uuid = req.query[String.self, at: configurationUUIDQueryKey]?
            .trimmingCharacters(in: .whitespacesAndNewlines)
        let name = req.query[String.self, at: configurationNameQueryKey]?
            .trimmingCharacters(in: .whitespacesAndNewlines)
        let requestedEndpoint = req.query[String.self, at: configurationEndpointQueryKey]?
            .trimmingCharacters(in: .whitespacesAndNewlines)
        let endpoint: String?
        if name?.caseInsensitiveCompare(ArendalsukaConfigurationPublisherContract.configurationName) == .orderedSame,
           requestedEndpoint?.caseInsensitiveCompare(ArendalsukaParticipantProgramContract.endpoint) == .orderedSame {
            // Preserve links issued before the official configuration moved to
            // its scaffold-owned publisher. This changes lookup location only;
            // the publisher Cell still enforces its Agreement and proof rules.
            endpoint = ArendalsukaConfigurationPublisherContract.endpoint
        } else {
            endpoint = requestedEndpoint
        }

        if let surfaceID, surfaceID.isEmpty == false {
            let hasCompetingLookup = [uuid, name, endpoint].contains { value in
                value?.isEmpty == false
            }
            var launch: Object = [
                "schema": .string(ScaffoldLaunchRegistryContract.launchSchema),
                "surfaceID": .string(surfaceID),
                "intent": .string("view")
            ]
            if hasCompetingLookup {
                launch["ambiguous"] = .bool(true)
            }
            return .object(["surfaceLaunch": .object(launch)])
        }

        var lookup: Object = [:]
        if let uuid, uuid.isEmpty == false {
            lookup["uuid"] = .string(uuid)
        }
        if let name, name.isEmpty == false {
            lookup["name"] = .string(name)
        }
        if let endpoint, endpoint.isEmpty == false {
            lookup["sourceCellEndpoint"] = .string(endpoint)
        }

        guard lookup.isEmpty == false else {
            return nil
        }

        return .object([
            "configurationLookup": .object(lookup)
        ])
    }

    static func requestedConfigurationTargetsPersonalChatHub(_ payload: ValueType?) -> Bool {
        guard case let .object(payloadObject)? = payload,
              case let .object(lookup)? = payloadObject["configurationLookup"] else {
            return false
        }
        if case let .string(endpoint)? = lookup["sourceCellEndpoint"] {
            return endpoint.trimmingCharacters(in: .whitespacesAndNewlines)
                .caseInsensitiveCompare(PersonalChatHubContract.endpoint) == .orderedSame
        }
        if case let .string(name)? = lookup["name"] {
            return name.trimmingCharacters(in: .whitespacesAndNewlines)
                .caseInsensitiveCompare("Co-Pilot Chat") == .orderedSame
        }
        return false
    }

    /// Materializes the requester's identity-unique chat hub while the web
    /// route still holds the BrowserClientIdentityVault-bound identity. The
    /// resolver remains the sole authority: it proves signing control, reuses
    /// an existing owner-bound hub, and persists a new mapping when absent.
    @discardableResult
    static func provisionPersonalChatHubForFirstUse(
        requester: Identity
    ) async throws -> PersonalChatHubCell {
        guard let resolver = CellBase.defaultCellResolver else {
            throw CellBaseError.noResolver
        }
        let resolved = try await resolver.cellAtEndpoint(
            endpoint: PersonalChatHubContract.endpoint,
            requester: requester
        )
        guard let hub = resolved as? PersonalChatHubCell,
              hub.cellScope == .identityUnique,
              hub.persistancy == .persistant else {
            throw Abort(
                .serviceUnavailable,
                reason: "Personal Chat Hub provisioning returned an invalid Cell contract."
            )
        }
        let mappings = await resolver.identityNamedCells(requester: requester)
        guard mappings[requester.uuid]?[PersonalChatHubContract.cellName] == hub.uuid else {
            throw Abort(
                .serviceUnavailable,
                reason: "Personal Chat Hub provisioning did not persist the requester-owned mapping."
            )
        }
        return hub
    }

    static func activeConferencePersonaID(
        requestedSelection: PortholeConferencePersonaSelection,
        storedConferencePersonaID: String?
    ) -> String? {
        switch requestedSelection {
        case .inheritStored:
            return storedConferencePersonaID
        case .clearStored:
            return nil
        case .persona(let personaID):
            return personaID
        }
    }

    static func shouldResetSession(
        requestedSelection: PortholeConferencePersonaSelection,
        storedConferencePersonaID: String?
    ) -> Bool {
        switch requestedSelection {
        case .inheritStored:
            return false
        case .clearStored:
            return storedConferencePersonaID != nil
        case .persona(let requestedPersonaID):
            return requestedPersonaID != storedConferencePersonaID
        }
    }

    static func persistConferencePersonaID(_ personaID: String?, in req: Request) {
        if conferencePersonasEnabled(in: req), let personaID, personaID.isEmpty == false {
            req.session.data[conferencePersonaSessionKey] = personaID
        } else {
            req.session.data[conferencePersonaSessionKey] = nil
        }
    }

    static func persistConferencePersonaWarning(_ warning: String?, in req: Request) {
        if let warning = warning?.trimmingCharacters(in: .whitespacesAndNewlines),
           warning.isEmpty == false {
            req.session.data[conferencePersonaWarningSessionKey] = warning
        } else {
            req.session.data[conferencePersonaWarningSessionKey] = nil
        }
    }

    static func resolveRequesterIdentity(
        for webUser: FidoUser,
        identityVault: BrowserClientIdentityVault,
        activeConferencePersonaID: String?
    ) async throws -> Identity {
        _ = activeConferencePersonaID
        return try await identityVault.identity(for: webUser)
    }

    static func requesterIdentity(
        for session: WebCellEmbeddings,
        fallbackRequester: Identity? = nil
    ) async -> Identity {
        let sessionOwner = await session.owner
        if await identityIsBoundToAttachedHomeVault(sessionOwner) {
            return sessionOwner
        }
        if let fallbackRequester,
           identitiesHaveSameSigningPublicKey(sessionOwner, fallbackRequester),
           await identityIsBoundToAttachedHomeVault(fallbackRequester) {
            return fallbackRequester
        }
        return sessionOwner
    }

    static func registerPublicRequesterIdentity(_ identity: Identity) async {
        guard let vaporVault = CellBase.defaultIdentityVault as? VaporIdentityVault else {
            return
        }
        await vaporVault.addVisitingIdentity(identity: publicIdentitySnapshot(identity))
    }

    static func publicIdentitySnapshot(_ identity: Identity) -> Identity {
        let snapshot = Identity(identity.uuid, displayName: identity.displayName, identityVault: nil)
        snapshot.publicSecureKey = identity.publicSecureKey
        snapshot.publicKeyAgreementSecureKey = identity.publicKeyAgreementSecureKey
        snapshot.grants = identity.grants
        snapshot.properties = nil
        snapshot.homeVaultReference = identity.homeVaultReference
        return snapshot
    }

    private static func identitiesHaveSameSigningPublicKey(_ lhs: Identity, _ rhs: Identity) -> Bool {
        guard
            let lhsKey = lhs.publicSecureKey,
            let rhsKey = rhs.publicSecureKey,
            lhsKey.algorithm == rhsKey.algorithm,
            lhsKey.curveType == rhsKey.curveType,
            let lhsCompressed = lhsKey.compressedKey,
            lhsCompressed.isEmpty == false,
            let rhsCompressed = rhsKey.compressedKey,
            rhsCompressed.isEmpty == false
        else {
            return false
        }
        return lhsCompressed == rhsCompressed
    }

    static func ownerRequester(for cell: GeneralCell, requester: Identity) async -> Identity {
        _ = cell
        // The cell owner is metadata, never a signing or authorization proxy for
        // the web requester. GeneralCell/Resolver must evaluate the real actor.
        return requester
    }

    static func sessionRequiresConferencePersonaRefresh(
        _ session: WebCellEmbeddings,
        activeConferencePersonaID: String?
    ) async -> Bool {
        let sessionPersonaID = session.conferencePersonaId
        guard sessionPersonaID == activeConferencePersonaID else {
            return true
        }

        return false
    }

    static func bootstrapValue(
        controlCell: OrchestratorCell,
        requester: Identity,
        sessionId: String,
        conferencePersonaId: String? = nil,
        conferencePersonaWarning: String? = nil,
        includeImplicitDefaultChatWorkbench: Bool = true
    ) async throws -> ValueType {
        let bootstrapStartedAt = Date()
        var stateObject: Object = [:]
        var referenceTimings = ValueTypeList()
        var unavailableKeypathsByReference: Object = [:]
        let controlCellOwner = await ownerRequester(for: controlCell, requester: requester)
        let storedConfiguration = await repairedActiveConfigurationIfNeeded(
            controlCell.getCellConfiguration(),
            controlCell: controlCell,
            requester: requester,
            loadRequester: controlCellOwner
        )
        let configuration: CellConfiguration?
        if let storedConfiguration {
            configuration = await EditableCellConfigurationOverlayResolver.overlay(
                configuration: storedConfiguration,
                requester: requester
            )
        } else {
            configuration = nil
        }
        let effectiveConfiguration = includeImplicitDefaultChatWorkbench
            ? configurationWithDefaultChatWorkbench(configuration)
            : configuration
        if configurationUsesAdminControlPlane(effectiveConfiguration) {
            _ = await AdminEntityProofPersistenceSupport.restoreAcceptedCredentials(
                on: requester
            )
        }
        let projectedKeypathsByLabel = PortholeBootstrapProjection.readableReferenceKeypaths(for: effectiveConfiguration)
        let workspaceName = configuration?.name ?? effectiveConfiguration?.name ?? "Current Porthole workspace"
        var accessRequirements = [BootstrapAccessRequirement]()
        if let cellConfiguration = effectiveConfiguration,
           let references = cellConfiguration.cellReferences {
            for reference in references {
                let resolvedReference = resolvedSharedWorkbenchReference(
                    for: reference,
                    label: reference.label,
                    configuration: effectiveConfiguration
                )
                let referenceStartedAt = Date()
                var cellState: Object = [:]
                let referenceResolutionRequester = await referenceResolutionRequester(
                    for: resolvedReference,
                    label: reference.label,
                    configuration: effectiveConfiguration,
                    requester: requester,
                    referenceLookupRequester: controlCellOwner
                )
                let usesRequesterOwnedTarget = isRequesterOwnedReference(resolvedReference, label: reference.label)
                let usesSharedWorkbenchOwnerTarget = isSharedWorkbenchConfiguration(effectiveConfiguration)
                    && isSharedWorkbenchOwnerTargetLabel(reference.label)
                let usesDirectConferenceTarget = usesRequesterOwnedTarget
                    || isRequesterScopedConferencePreviewReference(resolvedReference)
                let attachedTarget: Meddle?
                if usesDirectConferenceTarget || usesSharedWorkbenchOwnerTarget {
                    attachedTarget = nil
                } else {
                    attachedTarget = await controlCell.getEmitterWithLabel(reference.label, requester: controlCellOwner) as? Meddle
                }
                let endpointScopedTarget: Meddle?
                if isEndpointScopedUtilityReference(resolvedReference) {
                    endpointScopedTarget = await inspectionTargetCell(
                        for: resolvedReference,
                        requester: referenceResolutionRequester
                    )
                } else {
                    endpointScopedTarget = nil
                }
                let directConferenceTarget: Meddle?
                if usesDirectConferenceTarget {
                    directConferenceTarget = await inspectionTargetCell(
                        for: resolvedReference,
                        requester: referenceResolutionRequester
                    )
                } else {
                    directConferenceTarget = nil
                }
                let sharedWorkbenchTarget: Meddle?
                if usesSharedWorkbenchOwnerTarget {
                    sharedWorkbenchTarget = await inspectionTargetCell(
                        for: resolvedReference,
                        requester: referenceResolutionRequester
                    )
                } else {
                    sharedWorkbenchTarget = nil
                }
                let usesDirectResolvedTarget = endpointScopedTarget != nil
                    || directConferenceTarget != nil
                    || sharedWorkbenchTarget != nil
                if let meddle = endpointScopedTarget ?? directConferenceTarget ?? sharedWorkbenchTarget ?? attachedTarget {
                    var activeTarget = meddle
                    var ownerLookupRequester = usesDirectResolvedTarget ? referenceResolutionRequester : controlCellOwner
                    await ensurePortholeRuntimeBindingsIfNeeded(activeTarget, requester: ownerLookupRequester)
                    var referenceRequester = await attachedReferenceRequester(
                        for: activeTarget,
                        label: reference.label,
                        configuration: effectiveConfiguration,
                        requester: requester,
                        referenceLookupRequester: ownerLookupRequester
                    )
                    var inspectionTarget = await inspectionTargetCell(
                        for: resolvedReference,
                        requester: referenceResolutionRequester
                    ) ?? activeTarget
                    await ensurePortholeRuntimeBindingsIfNeeded(
                        inspectionTarget,
                        requester: referenceResolutionRequester
                    )
                    var hasProofRequirement = targetHasProofRequirement(inspectionTarget)
                    var projection = await bootstrapProjectionState(
                        targetCell: activeTarget,
                        projectedKeypaths: projectedKeypathsByLabel[reference.label] ?? [],
                        requester: referenceRequester,
                        hasProofRequirement: hasProofRequirement,
                        includeEditor: true
                    )
                    if let denialReason = projection.denialReason,
                       isIdentityReferenceMismatchDescription(denialReason),
                       await ConferencePreviewWrapperResolverSupport.resetStalePreviewMappingsIfNeeded(
                        for: resolvedReference.endpoint,
                        requester: requester
                       ),
                       let recoveredTarget = await inspectionTargetCell(
                        for: resolvedReference,
                        requester: referenceResolutionRequester
                       ) {
                        activeTarget = recoveredTarget
                        ownerLookupRequester = referenceResolutionRequester
                        await ensurePortholeRuntimeBindingsIfNeeded(activeTarget, requester: ownerLookupRequester)
                        referenceRequester = await attachedReferenceRequester(
                            for: activeTarget,
                            label: reference.label,
                            configuration: effectiveConfiguration,
                            requester: requester,
                            referenceLookupRequester: ownerLookupRequester
                        )
                        inspectionTarget = activeTarget
                        await ensurePortholeRuntimeBindingsIfNeeded(
                            inspectionTarget,
                            requester: referenceResolutionRequester
                        )
                        hasProofRequirement = targetHasProofRequirement(inspectionTarget)
                        projection = await bootstrapProjectionState(
                            targetCell: activeTarget,
                            projectedKeypaths: projectedKeypathsByLabel[reference.label] ?? [],
                            requester: referenceRequester,
                            hasProofRequirement: hasProofRequirement,
                            includeEditor: true
                        )
                    }
                    cellState["connected"] = .bool(true)
                    for (key, value) in projection.cellState {
                        cellState[key] = value
                    }
                    let nestedRequirements = await nestedAccessRequirements(
                        from: resolvedReference,
                        targetCell: inspectionTarget,
                        cellState: cellState,
                        projectedKeypaths: projectedKeypathsByLabel[reference.label] ?? [],
                        workspaceName: workspaceName,
                        inspectionRequester: referenceRequester
                    )
                    if nestedRequirements.isEmpty == false {
                        accessRequirements.append(contentsOf: nestedRequirements)
                    }
                    var deniedKeypaths = projection.deniedKeypaths
                    var unavailableKeypaths = projection.unavailableKeypaths
                    var denialReason = projection.denialReason

                    if shouldRedactProjectedStateForRequester(reference: resolvedReference) {
                        let requesterProjection = await bootstrapProjectionState(
                            targetCell: inspectionTarget,
                            projectedKeypaths: projectedKeypathsByLabel[reference.label] ?? [],
                            requester: requester,
                            hasProofRequirement: hasProofRequirement,
                            includeEditor: false
                        )
                        if requesterProjection.deniedKeypaths.isEmpty == false {
                            redactDeniedKeypaths(requesterProjection.deniedKeypaths, from: &cellState)
                            deniedKeypaths = uniqueKeypaths(deniedKeypaths + requesterProjection.deniedKeypaths)
                            denialReason = denialReason ?? requesterProjection.denialReason
                        }
                        unavailableKeypaths = uniqueKeypaths(
                            unavailableKeypaths + requesterProjection.unavailableKeypaths
                        )
                    }

                    if nestedRequirements.isEmpty,
                       deniedKeypaths.isEmpty,
                       cellState["state"] == nil,
                       hasProofRequirement {
                        deniedKeypaths = uniqueKeypaths((projectedKeypathsByLabel[reference.label] ?? []) + ["state"])
                        denialReason = denialReason ?? "Proof requirement is not satisfied yet."
                    }

                    if nestedRequirements.isEmpty,
                       deniedKeypaths.isEmpty == false {
                        accessRequirements.append(
                            await makeAccessRequirement(
                                reference: reference,
                                targetCell: inspectionTarget,
                                deniedKeypaths: deniedKeypaths,
                                denialReason: denialReason ?? "Access denied.",
                                workspaceName: workspaceName,
                                inspectionRequester: referenceRequester
                            )
                        )
                    }
                    if unavailableKeypaths.isEmpty == false {
                        unavailableKeypathsByReference[reference.label] = .list(
                            unavailableKeypaths.map(ValueType.string)
                        )
                    }
                } else {
                    cellState["connected"] = .bool(false)
                    if let inspectionTarget = await inspectionTargetCell(
                        for: reference,
                        requester: referenceResolutionRequester
                    ) {
                        await ensurePortholeRuntimeBindingsIfNeeded(
                            inspectionTarget,
                            requester: referenceResolutionRequester
                        )
                        let referenceRequester = await attachedReferenceRequester(
                            for: inspectionTarget,
                            label: reference.label,
                            configuration: effectiveConfiguration,
                            requester: requester,
                            referenceLookupRequester: referenceResolutionRequester
                        )
                        let projectedKeypaths = projectedKeypathsByLabel[reference.label] ?? []
                        let hasProofRequirement = targetHasProofRequirement(inspectionTarget)
                        let projection = await bootstrapProjectionState(
                            targetCell: inspectionTarget,
                            projectedKeypaths: projectedKeypaths,
                            requester: referenceRequester,
                            hasProofRequirement: hasProofRequirement,
                            includeEditor: false
                        )
                        for (key, value) in projection.cellState {
                            cellState[key] = value
                        }
                        let nestedRequirements = await nestedAccessRequirements(
                            from: reference,
                            targetCell: inspectionTarget,
                            cellState: cellState,
                            projectedKeypaths: projectedKeypaths,
                            workspaceName: workspaceName,
                            inspectionRequester: referenceRequester
                        )
                        if nestedRequirements.isEmpty == false {
                            accessRequirements.append(contentsOf: nestedRequirements)
                        }

                        var deniedKeypaths = projection.deniedKeypaths
                        var unavailableKeypaths = projection.unavailableKeypaths
                        var denialReason = projection.denialReason
                        if shouldRedactProjectedStateForRequester(reference: reference) {
                            let requesterProjection = await bootstrapProjectionState(
                                targetCell: inspectionTarget,
                                projectedKeypaths: projectedKeypaths,
                                requester: requester,
                                hasProofRequirement: hasProofRequirement,
                                includeEditor: false
                            )
                            if requesterProjection.deniedKeypaths.isEmpty == false {
                                redactDeniedKeypaths(requesterProjection.deniedKeypaths, from: &cellState)
                                deniedKeypaths = uniqueKeypaths(deniedKeypaths + requesterProjection.deniedKeypaths)
                                denialReason = denialReason ?? requesterProjection.denialReason
                            }
                            unavailableKeypaths = uniqueKeypaths(
                                unavailableKeypaths + requesterProjection.unavailableKeypaths
                            )
                        }
                        if nestedRequirements.isEmpty,
                           deniedKeypaths.isEmpty,
                           hasProofRequirement,
                           cellState["state"] == nil {
                            deniedKeypaths = uniqueKeypaths(projectedKeypaths + ["state"])
                            denialReason = denialReason ?? "Proof requirement is not satisfied yet."
                        }

                        if nestedRequirements.isEmpty,
                           deniedKeypaths.isEmpty == false {
                            accessRequirements.append(
                                await makeAccessRequirement(
                                    reference: reference,
                                    targetCell: inspectionTarget,
                                    deniedKeypaths: deniedKeypaths,
                                    denialReason: denialReason ?? "Reference could not be attached until access is approved.",
                                    workspaceName: workspaceName,
                                    inspectionRequester: referenceRequester
                                )
                            )
                        }
                        if unavailableKeypaths.isEmpty == false {
                            unavailableKeypathsByReference[reference.label] = .list(
                                unavailableKeypaths.map(ValueType.string)
                            )
                        }
                    }
                }
                stateObject[reference.label] = .object(cellState)
                referenceTimings.append(.object([
                    "label": .string(reference.label),
                    "endpoint": .string(reference.endpoint),
                    "connected": cellState["connected"] ?? .bool(false),
                    "durationMs": .float(Date().timeIntervalSince(referenceStartedAt) * 1_000)
                ]))
            }
        }
        accessRequirements = await visibleAccessRequirements(
            accessRequirements,
            sessionId: sessionId
        )
        await accessRequirementDecisionStore.setActiveFingerprint(
            accessRequirements.first?.fingerprint,
            sessionId: sessionId
        )

        if let statuses = try? await controlCell.attachedStatuses(requester: requester) {
            let list: ValueTypeList = statuses.map { status in
                .object([
                    "name": .string(status.name),
                    "connected": .bool(status.connected),
                    "active": .bool(status.active)
                ])
            }
            stateObject["$porthole"] = .object([
                "connectionStatuses": .list(list)
            ])
        }

        let notificationSummary = await notificationSummaryValue(requester: requester)
        var portholeMeta: Object
        if case let .object(existing)? = stateObject["$porthole"] {
            portholeMeta = existing
        } else {
            portholeMeta = [:]
        }
        if accessRequirements.isEmpty == false {
            portholeMeta["accessRequirements"] = .list(accessRequirements.map(\.value))
            portholeMeta["accessRequirementCount"] = .integer(accessRequirements.count)
            portholeMeta["accessRequirementSummary"] = .string(accessRequirementSummary(for: accessRequirements))
            portholeMeta["primaryAccessRequirement"] = accessRequirements[0].value
            portholeMeta["requesterIdentityToken"] = .string((try? requester.did()) ?? "identity_proof_required")
            portholeMeta["requesterDisplayName"] = .string(requester.displayName)
            if accessRequirements[0].paymentResolutionRequired {
                portholeMeta["paymentResolution"] = .object(await paymentResolutionObject(
                    for: accessRequirements[0],
                    requester: requester
                ))
            }
            await preconfigureAccessRequirementPrompt(
                from: accessRequirements[0],
                requester: requester
            )
        }
        if let sharedAccessVerification = await WorkbenchAccessGrantCell.requesterSharedAccessVerification(
            configuration: effectiveConfiguration,
            requester: requester
        ) {
            portholeMeta["sharedWorkbenchAccess"] = sharedAccessVerification
        }
        portholeMeta["notifications"] = notificationSummary
        stateObject["$porthole"] = .object(portholeMeta)

        let menusObject = bootstrapMenuSummaryObject()
        let availableConfigurations = bootstrapAvailableConfigurationSummaryList()

        let bootstrapConfiguration = configurationWithAccessRequirementOverlay(
            effectiveConfiguration,
            accessRequirements: accessRequirements
        )
        let configurationValue: ValueType = bootstrapConfiguration.map { .cellConfiguration($0) } ?? .null
        let editableConfigurationState = await currentEditableState(
            for: configuration,
            requester: requester
        )
        let committedEditorBaseConfiguration = editorCommittedConfiguration(
            currentConfiguration: configuration,
            editableConfigurationState: editableConfigurationState
        )
        let committedEditorConfiguration = includeImplicitDefaultChatWorkbench
            ? configurationWithDefaultChatWorkbench(committedEditorBaseConfiguration)
            : committedEditorBaseConfiguration
        let editorState = PortholeEditorSessionStore.shared.sync(
            sessionId: sessionId,
            committedConfiguration: committedEditorConfiguration,
            committedSourceRevision: editableConfigurationState?.revision
        )
        let editorStateValue = makeEditorStateValue(
            editorState,
            includeDocumentSnapshots: true,
            editableConfigurationState: editableConfigurationState
        )
        let legacyEditorValue = makeLegacyEditorValue(editorState)
        let componentPaletteValue = encodeCodableValue(PortholeWebComponentCatalog.defaultItems())
        let requesterValue = requesterSnapshot(
            requester,
            conferencePersonaId: conferencePersonaId,
            conferencePersonaWarning: conferencePersonaWarning
        )
        let bridgePresenceValue = bridgePresenceValue(for: requester)
        portholeMeta["bootstrapDiagnostics"] = .object([
            "schemaVersion": .string("porthole.bootstrap.diagnostics.v1"),
            "durationMs": .float(Date().timeIntervalSince(bootstrapStartedAt) * 1_000),
            "referenceCount": .integer(referenceTimings.count),
            "referenceTimings": .list(referenceTimings),
            "unavailableKeypathsByReference": .object(unavailableKeypathsByReference),
            "statePayloadBytesEstimate": encodedPayloadByteCount(.object(stateObject)).map { .integer($0) } ?? .string("unavailable")
        ])
        stateObject["$porthole"] = .object(portholeMeta)

        let portholeState: Object = [
            "sessionId": .string(sessionId),
            "configuration": configurationValue,
            "state": .object(stateObject),
            "notifications": notificationSummary,
            "menus": .object(menusObject),
            "availableConfigurations": availableConfigurations,
            "componentPalette": componentPaletteValue,
            "requester": requesterValue,
            "bridgePresence": bridgePresenceValue
        ]

        return .object([
            "contractVersion": .string("porthole-web-v2"),
            "portholeState": .object(portholeState),
            "editorState": editorStateValue,
            "sessionId": .string(sessionId),
            "configuration": configurationValue,
            "state": .object(stateObject),
            "notifications": notificationSummary,
            "menus": .object(menusObject),
            "availableConfigurations": availableConfigurations,
            "componentPalette": componentPaletteValue,
            "requester": requesterValue,
            "bridgePresence": bridgePresenceValue,
            "editor": legacyEditorValue
        ])
    }

    private static func readBootstrapValue(
        from meddle: Meddle,
        keypath: String,
        requester: Identity
    ) async -> BootstrapReadResult {
        do {
            let value = try await meddle.get(keypath: keypath, requester: requester)
            if let denialReason = accessDenialReason(from: value) {
                return .accessDenied(denialReason)
            }
            return .value(value)
        } catch {
            let message = String(describing: error)
            if let proofReason = proofLookupFailureReason(from: .string(message)) {
                return .accessDenied(proofReason)
            }
            guard let denialReason = accessDenialReason(from: message) else {
                return .unavailable
            }
            return .accessDenied(denialReason)
        }
    }

    private static func encodedPayloadByteCount(_ value: ValueType) -> Int? {
        try? JSONEncoder().encode(value).count
    }

    private static func accessDenialReason(from value: ValueType) -> String? {
        guard case let .string(message) = value else { return nil }
        return accessDenialReason(from: message)
    }

    private static func accessDenialReason(from message: String) -> String? {
        let trimmed = message.trimmingCharacters(in: .whitespacesAndNewlines)
        guard trimmed.isEmpty == false else { return nil }
        let lowered = trimmed.lowercased()
        let denialMarkers = [
            "denied",
            "deniednogrant",
            "forbidden",
            "permission",
            "agreement",
            "no grant",
            "nogrant",
            "not authorized",
            "unauthorized",
            "authorization",
            "not readable",
            "explicit access"
        ]
        return denialMarkers.contains(where: lowered.contains) ? trimmed : nil
    }

    private static func targetHasProofRequirement(_ targetCell: Meddle) -> Bool {
        if targetCell is AgeProofDoorCell || targetCell is PaymentProofDoorCell {
            return true
        }
        guard let generalCell = targetCell as? GeneralCell else { return false }
        return generalCell.agreementTemplate.conditions.contains { condition in
            condition is ProvedClaimCondition
        }
    }

    private static func inspectionTargetCell(
        for reference: CellReference,
        requester: Identity
    ) async -> Meddle? {
        await inspectionTargetCell(
            endpoint: reference.endpoint,
            requester: requester
        )
    }

    private static func inspectionTargetCell(
        endpoint: String,
        requester: Identity
    ) async -> Meddle? {
        if endpoint == ArendalsukaAtlasImportAccessContract.resourceEndpoint {
            return try? await ArendalsukaCanonicalAtlasResolution.resolve(requester: requester)
        }
        if endpoint == PersonalChatHubContract.endpoint {
            return await PersonalChatHubCell(owner: requester)
        }
        if endpoint == ExecutablePurposeGroundingContract.endpoint {
            return await ExecutablePurposeGroundingCell(owner: requester)
        }
        if let resolver = CellBase.defaultCellResolver,
           let resolved = try? await resolver.cellAtEndpoint(
            endpoint: endpoint,
            requester: requester
           ) as? Meddle {
            return resolved
        }
        return nil
    }

    static func ensurePortholeRuntimeBindingsIfNeeded(
        _ target: Meddle,
        requester: Identity
    ) async {
        guard let bindingTarget = target as? PortholeRuntimeBindingEnsuring else {
            return
        }
        guard await runtimeBindingBootstrapStore.begin(bindingTarget, requester: requester) else {
            return
        }
        await bindingTarget.ensurePortholeRuntimeBindings(requester: requester)
        if let runtimeReady = target as? CellRuntimeReady {
            do {
                try await runtimeReady.ensureRuntimeReady()
            } catch {
                await runtimeBindingBootstrapStore.abort(bindingTarget, requester: requester)
                return
            }
        }
        await runtimeBindingBootstrapStore.finish(bindingTarget, requester: requester)
    }

    private static func redactDeniedKeypaths(_ keypaths: [String], from cellState: inout Object) {
        for keypath in keypaths {
            let trimmed = keypath.trimmingCharacters(in: .whitespacesAndNewlines)
            guard trimmed.isEmpty == false else { continue }
            let topLevelKey = trimmed.split(separator: ".", maxSplits: 1).first.map(String.init) ?? trimmed
            cellState[topLevelKey] = nil
        }
    }

    private static func bootstrapProjectionState(
        targetCell: Meddle,
        projectedKeypaths: [String],
        requester: Identity,
        hasProofRequirement: Bool,
        includeEditor: Bool
    ) async -> (cellState: Object, deniedKeypaths: [String], unavailableKeypaths: [String], denialReason: String?) {
        var cellState: Object = [:]
        var broadValuesByRoot = [String: ValueType]()
        var deniedKeypaths = [String]()
        var unavailableKeypaths = [String]()
        var denialReason: String?

        switch await readBootstrapValue(from: targetCell, keypath: "state", requester: requester) {
        case .value(let stateValue):
            if let proofReason = proofLookupFailureReason(from: stateValue) {
                deniedKeypaths.append("state")
                denialReason = denialReason ?? proofReason
            } else {
                cellState["state"] = stateValue
                broadValuesByRoot["state"] = stateValue
            }
        case .accessDenied(let reason):
            deniedKeypaths.append("state")
            denialReason = reason
        case .unavailable:
            if hasProofRequirement {
                deniedKeypaths.append("state")
                denialReason = denialReason ?? "Proof requirement is not satisfied yet."
            } else {
                unavailableKeypaths.append("state")
            }
            break
        }

        if includeEditor {
            switch await readBootstrapValue(from: targetCell, keypath: "editor", requester: requester) {
            case .value(let editorValue):
                cellState["editor"] = editorValue
                broadValuesByRoot["editor"] = editorValue
            case .accessDenied:
                break
            case .unavailable:
                unavailableKeypaths.append("editor")
            }
        }

        let filteredProjectedKeypaths = projectedKeypaths.filter { keypath in
            let trimmed = keypath.trimmingCharacters(in: .whitespacesAndNewlines)
            guard trimmed.isEmpty == false else { return false }
            return broadValuesByRoot.contains(where: { root, value in
                PortholeBootstrapProjection.rootValue(value, covers: trimmed, rootedAt: root)
            }) == false
        }

        for projectedKeypath in filteredProjectedKeypaths {
            switch await readBootstrapValue(from: targetCell, keypath: projectedKeypath, requester: requester) {
            case .value(let value):
                if let proofReason = proofLookupFailureReason(from: value) {
                    deniedKeypaths.append(projectedKeypath)
                    denialReason = denialReason ?? proofReason
                } else {
                    PortholeBootstrapProjection.merge(value, into: &cellState, at: projectedKeypath)
                }
            case .accessDenied(let reason):
                deniedKeypaths.append(projectedKeypath)
                denialReason = denialReason ?? reason
            case .unavailable:
                if hasProofRequirement {
                    deniedKeypaths.append(projectedKeypath)
                    denialReason = denialReason ?? "Proof requirement is not satisfied yet."
                } else {
                    unavailableKeypaths.append(projectedKeypath)
                }
                continue
            }
        }

        return (
            cellState,
            uniqueKeypaths(deniedKeypaths),
            uniqueKeypaths(unavailableKeypaths),
            denialReason
        )
    }

    private static func proofLookupFailureReason(from value: ValueType) -> String? {
        guard case let .string(message) = value else { return nil }
        let lowered = message.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        guard lowered.isEmpty == false else { return nil }
        guard lowered.contains("proof") else { return nil }
        if lowered.contains("missing key") || lowered.contains("no value found at") {
            return "Proof requirement is not satisfied yet."
        }
        return nil
    }

    private static func nestedAccessRequirements(
        from reference: CellReference,
        targetCell: Meddle,
        cellState: Object,
        projectedKeypaths: [String],
        workspaceName: String,
        inspectionRequester: Identity
    ) async -> [BootstrapAccessRequirement] {
        let descriptors = nestedRequirementDescriptors(
            for: targetCell,
            inspectionRequester: inspectionRequester
        )
        guard descriptors.isEmpty == false else { return [] }

        var requirements = [BootstrapAccessRequirement]()
        for descriptor in descriptors {
            let localRequestedKeypaths = translatedNestedRequestedKeypaths(
                from: projectedKeypaths,
                nestedStateKeypath: descriptor.nestedStateKeypath
            )
            guard localRequestedKeypaths.isEmpty == false else { continue }
            guard let nestedValue = nestedValue(at: descriptor.nestedStateKeypath, in: cellState),
                  nestedValueLooksUnavailable(nestedValue) else {
                continue
            }
            guard let (nestedTarget, nestedInspectionRequester) = await nestedInspectionTarget(
                for: descriptor,
                requester: inspectionRequester
            ) else {
                continue
            }

            let nestedReference = CellReference(
                endpoint: descriptor.endpoint,
                label: "\(reference.label).\(descriptor.labelSuffix)"
            )
            requirements.append(
                await makeAccessRequirement(
                    reference: nestedReference,
                    targetCell: nestedTarget,
                    deniedKeypaths: localRequestedKeypaths,
                    denialReason: descriptor.denialReason,
                    workspaceName: workspaceName,
                    inspectionRequester: nestedInspectionRequester,
                    resolutionHint: descriptor.resolutionHint,
                    resolutionRequesterUUID: descriptor.resolutionRequesterUUID,
                    resolutionRequesterDisplayName: descriptor.resolutionRequesterDisplayName
                )
            )
        }

        return requirements
    }

    private static func nestedRequirementDescriptors(
        for targetCell: Meddle,
        inspectionRequester: Identity
    ) -> [NestedRequirementDescriptor] {
        if targetCell is ConferenceAdminShellCell {
            return [
                NestedRequirementDescriptor(
                    nestedStateKeypath: "state.audienceDiscovery",
                    labelSuffix: "audienceDiscovery",
                    endpoint: "cell:///ConferenceAudienceDiscovery",
                    denialReason: "Audience discovery is blocked until the requester approves organizer access to the underlying discovery surface.",
                    resolutionHint: "conference-organizer",
                    resolutionRequesterUUID: nil,
                    resolutionRequesterDisplayName: ConferenceOrganizerIdentity.ownerDisplayName
                ),
                NestedRequirementDescriptor(
                    nestedStateKeypath: "state.accessRequests",
                    labelSuffix: "accessRequests",
                    endpoint: "cell:///ConferenceAccessRequest",
                    denialReason: "Audience access requests are blocked until the requester approves organizer access to the underlying request surface.",
                    resolutionHint: "conference-organizer",
                    resolutionRequesterUUID: nil,
                    resolutionRequesterDisplayName: ConferenceOrganizerIdentity.ownerDisplayName
                ),
                NestedRequirementDescriptor(
                    nestedStateKeypath: "state.sessionThread",
                    labelSuffix: "sessionThread",
                    endpoint: ConferenceSessionThreadBridge.endpoint,
                    denialReason: "Session thread is blocked until the requester approves access to the shared session thread surface.",
                    resolutionHint: "conference-session-thread-shared",
                    resolutionRequesterUUID: nil,
                    resolutionRequesterDisplayName: nil
                ),
                NestedRequirementDescriptor(
                    nestedStateKeypath: "state.sessionPolling",
                    labelSuffix: "sessionPolling",
                    endpoint: ConferenceSessionPollingBridge.endpoint,
                    denialReason: "Session polling is blocked until the requester approves access to the shared polling surface.",
                    resolutionHint: "conference-session-polling-shared",
                    resolutionRequesterUUID: nil,
                    resolutionRequesterDisplayName: nil
                )
            ]
        }

        if targetCell is ConferenceParticipantShellCell {
            return [
                NestedRequirementDescriptor(
                    nestedStateKeypath: "state.discovery",
                    labelSuffix: "discovery",
                    endpoint: "cell:///ConferenceEntityDiscovery",
                    denialReason: "Participant discovery is blocked until the requester approves access to the workspace owner's discovery surface.",
                    resolutionHint: nil,
                    resolutionRequesterUUID: inspectionRequester.uuid,
                    resolutionRequesterDisplayName: inspectionRequester.displayName
                ),
                NestedRequirementDescriptor(
                    nestedStateKeypath: "state.sessionThread",
                    labelSuffix: "sessionThread",
                    endpoint: ConferenceSessionThreadBridge.endpoint,
                    denialReason: "Session thread is blocked until the requester approves access to the shared session thread surface.",
                    resolutionHint: "conference-session-thread-shared",
                    resolutionRequesterUUID: nil,
                    resolutionRequesterDisplayName: nil
                ),
                NestedRequirementDescriptor(
                    nestedStateKeypath: "state.sessionPolling",
                    labelSuffix: "sessionPolling",
                    endpoint: ConferenceSessionPollingBridge.endpoint,
                    denialReason: "Session polling is blocked until the requester approves access to the shared polling surface.",
                    resolutionHint: "conference-session-polling-shared",
                    resolutionRequesterUUID: nil,
                    resolutionRequesterDisplayName: nil
                )
            ]
        }

        return []
    }

    private static func translatedNestedRequestedKeypaths(
        from projectedKeypaths: [String],
        nestedStateKeypath: String
    ) -> [String] {
        let normalizedPrefix = nestedStateKeypath.trimmingCharacters(in: .whitespacesAndNewlines)
        guard normalizedPrefix.isEmpty == false else { return [] }

        var localRequestedKeypaths = [String]()
        for projectedKeypath in projectedKeypaths {
            let normalizedProjected = projectedKeypath.trimmingCharacters(in: .whitespacesAndNewlines)
            guard normalizedProjected.isEmpty == false else { continue }
            if normalizedProjected == normalizedPrefix {
                localRequestedKeypaths.append("state")
            } else if normalizedProjected.hasPrefix("\(normalizedPrefix).") {
                let suffix = String(normalizedProjected.dropFirst(normalizedPrefix.count + 1))
                localRequestedKeypaths.append("state.\(suffix)")
            }
        }

        if localRequestedKeypaths.isEmpty == false,
           localRequestedKeypaths.contains("state") == false {
            localRequestedKeypaths.append("state")
        }
        return uniqueKeypaths(localRequestedKeypaths)
    }

    private static func nestedValue(at keypath: String, in object: Object) -> ValueType? {
        let components = keypath
            .split(separator: ".")
            .map(String.init)
            .filter { $0.isEmpty == false }
        guard components.isEmpty == false else { return nil }

        var current: ValueType = .object(object)
        for component in components {
            guard case let .object(currentObject) = current,
                  let next = currentObject[component] else {
                return nil
            }
            current = next
        }
        return current
    }

    private static func nestedValueLooksUnavailable(_ value: ValueType) -> Bool {
        guard case let .object(object) = value else { return false }
        let candidateStrings = [
            object["status"]?.string,
            object["headline"]?.string,
            object["intro"]?.string,
            object["nextAction"]?.string
        ].compactMap { $0?.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() }

        return candidateStrings.contains { candidate in
            candidate.contains("unavailable") || candidate.contains("could not be resolved")
        }
    }

    private static func nestedInspectionTarget(
        for descriptor: NestedRequirementDescriptor,
        requester: Identity
    ) async -> (Meddle, Identity)? {
        switch descriptor.resolutionHint {
        case "conference-organizer":
            guard let target = await inspectionTargetCell(
                endpoint: descriptor.endpoint,
                requester: requester
            ) else {
                return nil
            }
            return (target, requester)
        case "conference-session-thread-shared":
            guard let target = try? await ConferenceSessionThreadBridge.sharedCell(for: requester) else {
                return nil
            }
            return (target, requester)
        case "conference-session-polling-shared":
            guard let target = try? await ConferenceSessionPollingBridge.sharedCell(for: requester) else {
                return nil
            }
            return (target, requester)
        default:
            guard let target = await inspectionTargetCell(
                endpoint: descriptor.endpoint,
                requester: requester
            ) else {
                return nil
            }
            return (target, requester)
        }
    }

    private static func makeAccessRequirement(
        reference: CellReference,
        targetCell: Meddle,
        deniedKeypaths: [String],
        denialReason: String,
        workspaceName: String,
        inspectionRequester: Identity,
        resolutionHint: String? = nil,
        resolutionRequesterUUID: String? = nil,
        resolutionRequesterDisplayName: String? = nil
    ) async -> BootstrapAccessRequirement {
        let requestedKeypaths = uniqueKeypaths(deniedKeypaths)
        let publishedContract = await publishedAccessRequirementContract(
            from: targetCell,
            requestedKeypaths: requestedKeypaths,
            inspectionRequester: inspectionRequester
        )
        let details = await inferRequirementDetails(
            from: targetCell,
            requestedKeypaths: requestedKeypaths,
            inspectionRequester: inspectionRequester
        )
        let label = reference.label.trimmingCharacters(in: .whitespacesAndNewlines)
        let defaultSubjectLabel = label.isEmpty ? reference.endpoint : "Reference `\(label)`"
        let kind = publishedContract?.kind ?? details.kind
        let subjectLabel = publishedContract?.subjectLabel ?? defaultSubjectLabel
        let proofKeypath = publishedContract?.proofKeypath ?? details.proofKeypath
        let proofCredentialType = publishedContract?.proofCredentialType
            ?? details.proofCredentialType
            ?? adminProofCredentialType(for: proofKeypath)
        let admissionMode: String
        if kind == "prove" && AdminMetricsSupport.isScaffoldAdminProofKeypath(proofKeypath) {
            admissionMode = "admin_external_authorization"
        } else if kind == "prove" && isPaymentProofRequirement(
            proofKeypath: proofKeypath,
            proofCredentialType: proofCredentialType
        ) {
            admissionMode = "payment_required"
        } else {
            admissionMode = kind
        }
        let proofPrompt = publishedContract?.proofPrompt
            ?? details.proofPrompt
            ?? adminProofPrompt(for: proofKeypath)
        let agreementName: String
        let purpose: String
        if kind == "prove" {
            agreementName = "Allow \(workspaceName) after proof for \(label.isEmpty ? reference.endpoint : label)"
            purpose = proofPrompt
                ?? "The active skeleton in `\(workspaceName)` needs a proved claim at `\(details.proofKeypath ?? "identity.proofs...")` before `\(reference.endpoint)` can grant readable access to `\(details.grantKeypath)`."
        } else {
            agreementName = "Allow \(workspaceName) to read \(label.isEmpty ? reference.endpoint : label)"
            purpose = "The active skeleton in `\(workspaceName)` needs readable access to `\(reference.endpoint)` at `\(details.grantKeypath)` before it can render this reference."
        }
        return BootstrapAccessRequirement(
            kind: kind,
            referenceLabel: label.isEmpty ? reference.endpoint : label,
            sourceCellEndpoint: reference.endpoint,
            requestedKeypaths: requestedKeypaths,
            denialReason: denialReason,
            subjectLabel: subjectLabel,
            grantKeypath: publishedContract?.grantKeypath ?? details.grantKeypath,
            grantPermission: publishedContract?.grantPermission ?? details.grantPermission,
            agreementName: publishedContract?.agreementName ?? agreementName,
            purpose: publishedContract?.purpose ?? purpose,
            durationHours: publishedContract?.durationHours ?? 24,
            proofKeypath: proofKeypath,
            proofCredentialType: proofCredentialType,
            proofPrompt: proofPrompt,
            admissionMode: admissionMode,
            resolutionHint: resolutionHint,
            resolutionRequesterUUID: resolutionRequesterUUID,
            resolutionRequesterDisplayName: resolutionRequesterDisplayName
        )
    }

    private static func adminProofCredentialType(for proofKeypath: String?) -> String? {
        if AdminMetricsSupport.isAdminEntryProofKeypath(proofKeypath) {
            return "AdminEntryCredential"
        }
        if AdminMetricsSupport.adminRole(forProofKeypath: proofKeypath) != nil {
            return "AdminRoleCredential"
        }
        return nil
    }

    private static func configurationUsesAdminControlPlane(_ configuration: CellConfiguration?) -> Bool {
        guard let references = configuration?.cellReferences else { return false }
        let routing = AdminControlPlaneRouting.current
        let endpoints = Set([
            "AdminEntry",
            "AdminAccessRequests",
            "AdminResolverStats",
            "AdminStorageStats",
            "AdminHostMetrics",
            "AdminMetricsHistory",
            "AdminCellLifecycle",
            "AdminProcesses",
            "AdminOverview",
            "AdminNodeFleet",
            "AdminDeploymentSupervisor",
            "AdminRoleEnrollment",
            "AdminSecurityPolicy"
        ].map { routing.endpoint(for: $0) })
        return references.contains { endpoints.contains($0.endpoint) }
    }

    private static func isPaymentProofRequirement(
        proofKeypath: String?,
        proofCredentialType: String?
    ) -> Bool {
        let credentialType = proofCredentialType?
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        if credentialType == "paymentaccesscredential" {
            return true
        }

        let normalizedProofKeypath = proofKeypath?
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased() ?? ""
        return normalizedProofKeypath == PaymentGatePolicy.entityPaymentProofRoot ||
            normalizedProofKeypath.hasPrefix("\(PaymentGatePolicy.entityPaymentProofRoot).") ||
            normalizedProofKeypath == "proofs.payments" ||
            normalizedProofKeypath.hasPrefix("proofs.payments.")
    }

    private static func adminProofPrompt(for proofKeypath: String?) -> String? {
        if AdminMetricsSupport.isAdminEntryProofKeypath(proofKeypath) {
            return "Denne adminflaten krever admin entry. Be en eksisterende admin om å registrere identiteten, eller last opp en gyldig AdminEntryCredential."
        }
        if let role = AdminMetricsSupport.adminRole(forProofKeypath: proofKeypath) {
            return "Denne adminflaten krever rollen `\(role.rawValue)`. Be en admin utstede rollen, eller last opp en gyldig AdminRoleCredential."
        }
        return nil
    }

    private static func publishedAccessRequirementContract(
        from targetCell: Meddle,
        requestedKeypaths: [String],
        inspectionRequester: Identity
    ) async -> PublishedAccessRequirementContract? {
        guard let generalCell = targetCell as? GeneralCell else { return nil }
        // Contract descriptors are non-secret admission metadata. Read only
        // this descriptor surface with the exact proof-bearing local owner;
        // never reuse that authority for the referenced state or user action.
        let contractRequester = (try? await PaymentGateOwnerIdentitySupport.requireLocalSigningOwner(
            for: generalCell
        )) ?? inspectionRequester
        guard let contractsValue = try? await generalCell.get(
            keypath: "accessRequirementContracts",
            requester: contractRequester
        ), case let .list(items) = contractsValue else {
            return nil
        }

        let contracts = items.compactMap { parsePublishedAccessRequirementContract($0) }
        guard contracts.isEmpty == false else { return nil }
        // `state` is always included as an implicit root read for a referenced
        // cell. Prefer the concrete skeleton keypaths when they are present so
        // a narrow quote/proof contract cannot lose a score tie to that root.
        let concreteRequestedKeypaths = requestedKeypaths.filter {
            $0.trimmingCharacters(in: .whitespacesAndNewlines) != "state"
        }
        let matchingKeypaths = concreteRequestedKeypaths.isEmpty
            ? requestedKeypaths
            : concreteRequestedKeypaths
        return contracts
            .compactMap { contract -> (PublishedAccessRequirementContract, Int)? in
                guard let score = contractMatchScore(contract.requestedKeypaths, requestedKeypaths: matchingKeypaths) else {
                    return nil
                }
                return (contract, score)
            }
            .max(by: { $0.1 < $1.1 })?
            .0
            ?? contracts.first
    }

    private static func parsePublishedAccessRequirementContract(_ value: ValueType) -> PublishedAccessRequirementContract? {
        guard case let .object(object) = value,
              let grantKeypath = object["grantKeypath"]?.string,
              let grantPermission = object["grantPermission"]?.string else {
            return nil
        }

        let kind = object["kind"]?.string?.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() == "prove"
            ? "prove"
            : "grant"
        let requestedKeypaths: [String]
        if case let .list(items)? = object["requestedKeypaths"] {
            requestedKeypaths = items.compactMap(\.string).map {
                $0.trimmingCharacters(in: .whitespacesAndNewlines)
            }.filter { $0.isEmpty == false }
        } else {
            requestedKeypaths = []
        }

        return PublishedAccessRequirementContract(
            kind: kind,
            subjectLabel: object["subjectLabel"]?.string,
            grantKeypath: grantKeypath,
            grantPermission: grantPermission,
            agreementName: object["agreementName"]?.string,
            purpose: object["purpose"]?.string,
            durationHours: integerValue(from: object["durationHours"]),
            proofKeypath: object["proofKeypath"]?.string,
            proofCredentialType: object["proofCredentialType"]?.string,
            proofPrompt: object["proofPrompt"]?.string,
            requestedKeypaths: requestedKeypaths
        )
    }

    private static func integerValue(from value: ValueType?) -> Int? {
        guard let value else { return nil }
        switch value {
        case .integer(let integer):
            return integer
        case .number(let integer):
            return integer
        default:
            return nil
        }
    }

    private static func contractMatchScore(_ contractKeypaths: [String], requestedKeypaths: [String]) -> Int? {
        guard contractKeypaths.isEmpty == false else { return 0 }

        var bestScore: Int?
        for contractKeypath in contractKeypaths {
            let normalizedContract = contractKeypath.trimmingCharacters(in: .whitespacesAndNewlines)
            guard normalizedContract.isEmpty == false else { continue }
            for requestedKeypath in requestedKeypaths {
                let normalizedRequested = requestedKeypath.trimmingCharacters(in: .whitespacesAndNewlines)
                guard normalizedRequested.isEmpty == false else { continue }
                guard keypathMatches(contract: normalizedContract, requested: normalizedRequested) else { continue }
                let score = normalizedContract.split(separator: ".").count + normalizedRequested.split(separator: ".").count
                bestScore = max(bestScore ?? score, score)
            }
        }

        return bestScore
    }

    private static func keypathMatches(contract: String, requested: String) -> Bool {
        if contract == requested {
            return true
        }
        if requested.hasPrefix("\(contract).") {
            return true
        }
        if contract.hasPrefix("\(requested).") {
            return true
        }
        return false
    }

    private static func inferRequirementDetails(
        from targetCell: Meddle,
        requestedKeypaths: [String],
        inspectionRequester: Identity
    ) async -> InferredRequirementDetails {
        let fallbackGrantKeypath = requestedKeypaths.first ?? "state"
        let fallback = InferredRequirementDetails(
            kind: "grant",
            grantKeypath: fallbackGrantKeypath,
            grantPermission: "r---",
            proofKeypath: nil,
            proofCredentialType: nil,
            proofPrompt: nil
        )
        guard let generalCell = targetCell as? GeneralCell else {
            return fallback
        }

        let matchingGrant = generalCell.agreementTemplate.grants.first(where: { grant in
            requestedKeypaths.contains(grant.keypath)
        }) ?? generalCell.agreementTemplate.grants.first(where: { $0.keypath == fallbackGrantKeypath })
            ?? generalCell.agreementTemplate.grants.first

        guard let provedCondition = generalCell.agreementTemplate.conditions.compactMap({ condition in
            condition as? ProvedClaimCondition
        }).first else {
            return InferredRequirementDetails(
                kind: "grant",
                grantKeypath: matchingGrant?.keypath ?? fallbackGrantKeypath,
                grantPermission: matchingGrant?.permission.permissionString ?? "r---",
                proofKeypath: nil,
                proofCredentialType: nil,
                proofPrompt: nil
            )
        }

        var proofCredentialType: String?
        var proofPrompt: String?
        let targetOwner = await ownerRequester(for: generalCell, requester: inspectionRequester)
        if let stateValue = try? await generalCell.get(keypath: "state", requester: targetOwner),
           case let .object(stateObject) = stateValue {
            proofCredentialType = stateObject["requiredCredentialType"]?.string
            proofPrompt = stateObject["description"]?.string
        }

        return InferredRequirementDetails(
            kind: "prove",
            grantKeypath: matchingGrant?.keypath ?? fallbackGrantKeypath,
            grantPermission: matchingGrant?.permission.permissionString ?? "r---",
            proofKeypath: parseProofKeypath(from: provedCondition.statement),
            proofCredentialType: proofCredentialType,
            proofPrompt: proofPrompt
        )
    }

    private static func parseProofKeypath(from statement: String) -> String? {
        let components = statement.split(separator: "=", maxSplits: 1).map {
            String($0).trimmingCharacters(in: .whitespacesAndNewlines)
        }
        guard let first = components.first, first.isEmpty == false else { return nil }
        return first
    }

    private static func uniqueKeypaths(_ keypaths: [String]) -> [String] {
        var seen = Set<String>()
        var ordered = [String]()
        for keypath in keypaths {
            let trimmed = keypath.trimmingCharacters(in: .whitespacesAndNewlines)
            guard trimmed.isEmpty == false, seen.insert(trimmed).inserted else { continue }
            ordered.append(trimmed)
        }
        return ordered
    }

    private static func accessRequirementSummary(for requirements: [BootstrapAccessRequirement]) -> String {
        guard let first = requirements.first else { return "" }
        if first.externalApprovalRequired {
            if requirements.count == 1 {
                return "Adminflaten `\(first.referenceLabel)` er blokkert fordi denne identiteten mangler påkrevd scaffold admin-proof. Ingen admin-data er vist."
            }
            return "Denne arbeidsflaten har \(requirements.count) blokkerte admin-referanser. Start med tilgangskravet for `\(first.referenceLabel)`."
        }
        if first.paymentResolutionRequired {
            if requirements.count == 1 {
                return "Betalingsflaten `\(first.referenceLabel)` er blokkert til PaymentGate har utstedt en PaymentAccessCredential. Top-up og spend er eksplisitte brukerhandlinger."
            }
            return "Denne arbeidsflaten har \(requirements.count) betalingsblokkerte referanser. Start med betalingsvilkåret for `\(first.referenceLabel)`."
        }
        if first.kind == "prove" {
            if requirements.count == 1 {
                return "This workspace references `\(first.referenceLabel)`, but the requester must satisfy a proof requirement before the blocked content can render."
            }
            return "This workspace has \(requirements.count) blocked references. Start by satisfying the proof request for `\(first.referenceLabel)`."
        }
        if requirements.count == 1 {
            return "This workspace references `\(first.referenceLabel)`, but the requester must approve access before the blocked content can render."
        }
        return "This workspace has \(requirements.count) blocked references. Start by approving access for `\(first.referenceLabel)`."
    }

    private static func visibleAccessRequirements(
        _ requirements: [BootstrapAccessRequirement],
        sessionId: String
    ) async -> [BootstrapAccessRequirement] {
        guard sessionId.isEmpty == false, requirements.isEmpty == false else { return requirements }
        var visible = [BootstrapAccessRequirement]()
        for requirement in requirements {
            if await accessRequirementDecisionStore.isDismissed(requirement.fingerprint, sessionId: sessionId) == false {
                visible.append(requirement)
            }
        }
        return visible
    }

    private static func configurationWithAccessRequirementOverlay(
        _ configuration: CellConfiguration?,
        accessRequirements: [BootstrapAccessRequirement]
    ) -> CellConfiguration? {
        guard var configuration, accessRequirements.isEmpty == false else {
            return configuration
        }

        let overlay = accessRequirementOverlaySection(for: accessRequirements[0])
        if let skeleton = configuration.skeleton {
            switch skeleton {
            case .VStack(var stack):
                stack.elements.insert(overlay, at: 0)
                configuration.skeleton = .VStack(stack)
            default:
                configuration.skeleton = .VStack(SkeletonVStack(elements: [overlay, skeleton]))
            }
        } else {
            configuration.skeleton = .VStack(SkeletonVStack(elements: [overlay]))
        }

        return configuration
    }

    private static func accessRequirementOverlaySection(for requirement: BootstrapAccessRequirement) -> SkeletonElement {
        if requirement.externalApprovalRequired {
            return adminAccessRequirementOverlaySection()
        }
        if requirement.paymentResolutionRequired {
            return paymentAccessRequirementOverlaySection()
        }

        var primaryButtonModifiers = SkeletonModifiers()
        primaryButtonModifiers.padding = 8
        primaryButtonModifiers.background = "#4B2F18"
        primaryButtonModifiers.cornerRadius = 8
        primaryButtonModifiers.borderWidth = 1
        primaryButtonModifiers.borderColor = "#8D5A30"
        primaryButtonModifiers.foregroundColor = "#FFF4DB"
        primaryButtonModifiers.styleClasses = ["primary-action", "access-requirement-action"]

        var secondaryButtonModifiers = SkeletonModifiers()
        secondaryButtonModifiers.padding = 8
        secondaryButtonModifiers.background = "#F8E5CE"
        secondaryButtonModifiers.cornerRadius = 8
        secondaryButtonModifiers.borderWidth = 1
        secondaryButtonModifiers.borderColor = "#D2A471"
        secondaryButtonModifiers.foregroundColor = "#6A4321"
        secondaryButtonModifiers.styleClasses = ["secondary-action", "access-requirement-dismiss"]

        var approveButton = SkeletonButton(
            keypath: "porthole.approveAccessRequirement",
            label: "Approve now",
            payload: .bool(true)
        )
        approveButton.modifiers = primaryButtonModifiers

        var denyButton = SkeletonButton(
            keypath: "porthole.denyAccessRequirement",
            label: "Not now",
            payload: .bool(true)
        )
        denyButton.modifiers = secondaryButtonModifiers

        var section = SkeletonSection(
            header: .Text(SkeletonText(text: "Access approval needed")),
            content: [
                .Text(SkeletonText(keypath: "$porthole.accessRequirementSummary")),
                .Text(SkeletonText(keypath: "$porthole.primaryAccessRequirement.kind")),
                .Text(SkeletonText(keypath: "$porthole.primaryAccessRequirement.subjectLabel")),
                .Text(SkeletonText(keypath: "$porthole.primaryAccessRequirement.targetEndpoint")),
                .Text(SkeletonText(keypath: "$porthole.primaryAccessRequirement.purpose")),
                .Text(SkeletonText(keypath: "$porthole.primaryAccessRequirement.proofCredentialType")),
                .Text(SkeletonText(keypath: "$porthole.primaryAccessRequirement.proofKeypath")),
                .Text(SkeletonText(keypath: "$porthole.primaryAccessRequirement.denialReason")),
                .HStack(SkeletonHStack(elements: [
                    .Button(approveButton),
                    .Button(denyButton)
                ]))
            ]
        )
        var sectionModifiers = SkeletonModifiers()
        sectionModifiers.padding = 12
        sectionModifiers.background = "#FFF3E3"
        sectionModifiers.cornerRadius = 12
        sectionModifiers.borderWidth = 1
        sectionModifiers.borderColor = "#E1B27A"
        sectionModifiers.foregroundColor = "#4B2F18"
        sectionModifiers.styleClasses = ["access-requirement-banner"]
        section.modifiers = sectionModifiers
        return .Section(section)
    }

    private static func paymentAccessRequirementOverlaySection() -> SkeletonElement {
        func text(_ value: String, modifiers: SkeletonModifiers? = nil) -> SkeletonElement {
            var element = SkeletonText(text: value)
            element.modifiers = modifiers
            return .Text(element)
        }

        func boundText(_ keypath: String, modifiers: SkeletonModifiers? = nil) -> SkeletonElement {
            var element = SkeletonText(keypath: keypath)
            element.modifiers = modifiers
            return .Text(element)
        }

        var headingModifiers = SkeletonModifiers()
        headingModifiers.fontWeight = "700"
        headingModifiers.foregroundColor = "#12362B"

        var bodyModifiers = SkeletonModifiers()
        bodyModifiers.foregroundColor = "#20483B"

        var mutedModifiers = SkeletonModifiers()
        mutedModifiers.foregroundColor = "#4F6F64"

        var primaryButtonModifiers = SkeletonModifiers()
        primaryButtonModifiers.padding = 8
        primaryButtonModifiers.background = "#0B6B4F"
        primaryButtonModifiers.cornerRadius = 8
        primaryButtonModifiers.borderWidth = 1
        primaryButtonModifiers.borderColor = "#0B6B4F"
        primaryButtonModifiers.foregroundColor = "#F3FFF9"
        primaryButtonModifiers.styleClasses = ["primary-action", "access-requirement-action", "payment-access-use-quota-action"]

        var secondaryButtonModifiers = SkeletonModifiers()
        secondaryButtonModifiers.padding = 8
        secondaryButtonModifiers.background = "#E8F6EF"
        secondaryButtonModifiers.cornerRadius = 8
        secondaryButtonModifiers.borderWidth = 1
        secondaryButtonModifiers.borderColor = "#9CCDB8"
        secondaryButtonModifiers.foregroundColor = "#184536"
        secondaryButtonModifiers.styleClasses = ["secondary-action", "access-requirement-dismiss", "payment-access-dismiss-action"]

        var useQuotaButton = SkeletonButton(
            keypath: "porthole.useExistingPaymentQuota",
            label: "Bruk eksisterende kvote",
            payload: .bool(true)
        )
        useQuotaButton.modifiers = primaryButtonModifiers

        var topUpButton = SkeletonButton(
            keypath: "porthole.openPaymentTopUp",
            label: "Fyll på",
            payload: .bool(true)
        )
        topUpButton.modifiers = secondaryButtonModifiers

        var policyButton = SkeletonButton(
            keypath: "porthole.changePaymentPolicy",
            label: "Endre policy",
            payload: .bool(true)
        )
        policyButton.modifiers = secondaryButtonModifiers

        var dismissButton = SkeletonButton(
            keypath: "porthole.denyAccessRequirement",
            label: "Ikke nå",
            payload: .bool(true)
        )
        dismissButton.modifiers = secondaryButtonModifiers

        var section = SkeletonSection(
            header: nil,
            content: [
                text("Betaling eller brukskvote trengs", modifiers: headingModifiers),
                boundText("$porthole.accessRequirementSummary", modifiers: bodyModifiers),
                boundText("$porthole.primaryAccessRequirement.purpose", modifiers: bodyModifiers),
                boundText("$porthole.primaryAccessRequirement.proofCredentialType", modifiers: mutedModifiers),
                boundText("$porthole.primaryAccessRequirement.proofKeypath", modifiers: mutedModifiers),
                text("Denne flaten lager ikke betalingsproof selv. Brukeren må fylle på eksplisitt og la PaymentGate utstede credential etter spend.", modifiers: mutedModifiers),
                boundText("$porthole.paymentResolution.quoteSummary", modifiers: bodyModifiers),
                boundText("$porthole.paymentResolution.policy.policyBoundary", modifiers: mutedModifiers),
                boundText("$porthole.paymentResolution.policy.hardStopSummary", modifiers: mutedModifiers),
                .HStack(SkeletonHStack(elements: [
                    .Button(useQuotaButton),
                    .Button(topUpButton),
                    .Button(policyButton),
                    .Button(dismissButton)
                ]))
            ]
        )
        var sectionModifiers = SkeletonModifiers()
        sectionModifiers.padding = 12
        sectionModifiers.background = "#EEF9F3"
        sectionModifiers.cornerRadius = 12
        sectionModifiers.borderWidth = 1
        sectionModifiers.borderColor = "#9CCDB8"
        sectionModifiers.foregroundColor = "#12362B"
        sectionModifiers.styleClasses = ["access-requirement-banner", "payment-access-requirement-gate"]
        section.modifiers = sectionModifiers
        return .Section(section)
    }

    private static func adminAccessRequirementOverlaySection() -> SkeletonElement {
        func text(_ value: String, modifiers: SkeletonModifiers? = nil) -> SkeletonElement {
            var element = SkeletonText(text: value)
            element.modifiers = modifiers
            return .Text(element)
        }

        func boundText(_ keypath: String, modifiers: SkeletonModifiers? = nil) -> SkeletonElement {
            var element = SkeletonText(keypath: keypath)
            element.modifiers = modifiers
            return .Text(element)
        }

        var eyebrowModifiers = SkeletonModifiers()
        eyebrowModifiers.foregroundColor = "#1E7667"
        eyebrowModifiers.fontSize = 12
        eyebrowModifiers.fontWeight = "700"

        var titleModifiers = SkeletonModifiers()
        titleModifiers.foregroundColor = "#18201F"
        titleModifiers.fontSize = 18
        titleModifiers.fontWeight = "700"

        var bodyModifiers = SkeletonModifiers()
        bodyModifiers.foregroundColor = "#3C4643"
        bodyModifiers.fontSize = 13

        var mutedModifiers = SkeletonModifiers()
        mutedModifiers.foregroundColor = "#65726E"
        mutedModifiers.fontSize = 12

        var tokenModifiers = SkeletonModifiers()
        tokenModifiers.padding = 8
        tokenModifiers.background = "#F4F8F7"
        tokenModifiers.cornerRadius = 6
        tokenModifiers.borderWidth = 1
        tokenModifiers.borderColor = "#CFDCDA"
        tokenModifiers.foregroundColor = "#26312F"
        tokenModifiers.fontSize = 12
        tokenModifiers.minimumScaleFactor = 0.75

        var primaryButtonModifiers = SkeletonModifiers()
        primaryButtonModifiers.padding = 8
        primaryButtonModifiers.background = "#0F6B5D"
        primaryButtonModifiers.cornerRadius = 6
        primaryButtonModifiers.borderWidth = 1
        primaryButtonModifiers.borderColor = "#0B554B"
        primaryButtonModifiers.foregroundColor = "#FFFFFF"
        primaryButtonModifiers.styleClasses = ["primary-action", "access-requirement-action", "admin-access-request-action"]

        var secondaryButtonModifiers = SkeletonModifiers()
        secondaryButtonModifiers.padding = 8
        secondaryButtonModifiers.background = "#F7FAF9"
        secondaryButtonModifiers.cornerRadius = 6
        secondaryButtonModifiers.borderWidth = 1
        secondaryButtonModifiers.borderColor = "#C9D6D3"
        secondaryButtonModifiers.foregroundColor = "#33413E"
        secondaryButtonModifiers.styleClasses = ["secondary-action", "access-requirement-dismiss", "admin-access-dismiss-action"]

        var uploadModifiers = SkeletonModifiers()
        uploadModifiers.padding = 10
        uploadModifiers.background = "#FBFCFC"
        uploadModifiers.cornerRadius = 6
        uploadModifiers.borderWidth = 1
        uploadModifiers.borderColor = "#DDE6E4"

        var requestButton = SkeletonButton(
            keypath: "porthole.requestAccessRequirement",
            label: "Be om tilgang",
            payload: .bool(true)
        )
        requestButton.modifiers = primaryButtonModifiers

        var denyButton = SkeletonButton(
            keypath: "porthole.denyAccessRequirement",
            label: "Ikke nå",
            payload: .bool(true)
        )
        denyButton.modifiers = secondaryButtonModifiers

        var credentialUpload = SkeletonFileUpload(
            title: "Last opp admin-bevis",
            helperText: "Kun JSON-credential. Ikke last opp private keys, seed phrases eller API tokens.",
            actionKeypath: "porthole.submitAccessRequirementCredential",
            acceptedContentTypes: ["application/json", "text/json", "text/plain"],
            allowsMultiple: false,
            supportsDrop: true,
            emptyTitle: "Ingen credential valgt",
            emptyMessage: "Velg en AdminEntryCredential eller AdminRoleCredential.",
            maxSizeBytes: 128_000,
            uploadMode: "base64",
            submitOnSelection: true
        )
        credentialUpload.modifiers = uploadModifiers

        var section = SkeletonSection(
            header: text("Admin-tilgang mangler", modifiers: titleModifiers),
            content: [
                text("Tilgang stoppet", modifiers: eyebrowModifiers),
                boundText("$porthole.accessRequirementSummary", modifiers: bodyModifiers),
                boundText("$porthole.primaryAccessRequirement.proofPrompt", modifiers: bodyModifiers),
                boundText("$porthole.primaryAccessRequirement.proofCredentialType", modifiers: mutedModifiers),
                boundText("$porthole.primaryAccessRequirement.subjectLabel", modifiers: mutedModifiers),
                boundText("$porthole.primaryAccessRequirement.denialReason", modifiers: mutedModifiers),
                text("Identity-token for forespørsel", modifiers: mutedModifiers),
                boundText("$porthole.requesterIdentityToken", modifiers: tokenModifiers),
                .HStack(SkeletonHStack(elements: [
                    .Button(requestButton),
                    .Button(denyButton)
                ])),
                .FileUpload(credentialUpload)
            ]
        )
        var sectionModifiers = SkeletonModifiers()
        sectionModifiers.padding = 14
        sectionModifiers.background = "#FFFFFF"
        sectionModifiers.cornerRadius = 8
        sectionModifiers.borderWidth = 1
        sectionModifiers.borderColor = "#C9D6D3"
        sectionModifiers.foregroundColor = "#18201F"
        sectionModifiers.styleClasses = ["access-requirement-banner", "admin-access-requirement-gate"]
        section.modifiers = sectionModifiers
        return .Section(section)
    }

    private static func paymentResolutionObject(
        for requirement: BootstrapAccessRequirement,
        requester: Identity
    ) async -> Object {
        let resourceID = paymentResourceID(
            sourceCellEndpoint: requirement.sourceCellEndpoint,
            proofKeypath: requirement.proofKeypath
        )
        let quote = await paymentQuoteObject(resourceID: resourceID, requester: requester)
        let policy = await requesterPaymentPolicyObject(requester: requester)
        return [
            "status": .string("blocked"),
            "resourceID": .string(resourceID),
            "identityDomain": .string(
                await PaymentGateOwnerIdentitySupport.keyBoundIdentityDomain(for: requester)
                    ?? "identity_proof_required"
            ),
            "topUpPath": .string("/chat-mvp?topup=1"),
            "quote": .object(quote),
            "quoteSummary": .string(paymentQuoteSummary(resourceID: resourceID, quote: quote)),
            "policy": .object(policy),
            "useExistingQuotaAction": .string("porthole.useExistingPaymentQuota"),
            "topUpAction": .string("porthole.openPaymentTopUp"),
            "policyAction": .string("porthole.changePaymentPolicy")
        ]
    }

    private static func executePaymentRequirementAction(
        sessionId: String,
        mode: String,
        payload: ValueType,
        requester: Identity
    ) async throws -> ValueType {
        guard let requirement = try await promptRequirementObject(requester: requester),
              boolValue(requirement["paymentResolutionRequired"]) == true else {
            return .object([
                "status": .string("no_payment_requirement"),
                "message": .string("Ingen aktivt betalingskrav er tilgjengelig i denne Porthole-sesjonen.")
            ])
        }

        let resourceID = paymentResourceID(
            sourceCellEndpoint: stringValue(requirement["targetEndpoint"]) ?? stringValue(requirement["sourceCellEndpoint"]) ?? "",
            proofKeypath: stringValue(requirement["proofKeypath"])
        )

        switch mode {
        case "use_existing_quota":
            guard let (gate, paymentRequester) = await paymentGateTarget(requester: requester),
                  let identityDomain = await PaymentGateOwnerIdentitySupport.keyBoundIdentityDomain(for: requester) else {
                return .object([
                    "status": .string("authorization_required"),
                    "reasonCode": .string("proof_required"),
                    "requiredAction": .string("restore_identity_or_link_scaffold"),
                    "message": .string("Betalingshandlingen krever at identitetens private nøkkel er tilgjengelig i riktig home vault.")
                ])
            }

            let idempotencyKey = "porthole|\(sessionId)|\(requester.uuid)|\(resourceID)"
            let result = try await gate.set(
                keypath: "enter",
                value: .object([
                    "identityDomain": .string(identityDomain),
                    "resourceID": .string(resourceID),
                    "idempotencyKey": .string(idempotencyKey)
                ]),
                requester: paymentRequester
            ) ?? .null

            if case let .object(object) = result,
               object["status"]?.string == "granted" {
                return .object([
                    "status": .string("payment_credential_issued"),
                    "message": .string("PaymentGate trakk fra eksisterende brukskvote og utstedte PaymentAccessCredential. Last arbeidsflaten på nytt hvis innholdet ikke åpnes automatisk."),
                    "resourceID": .string(resourceID),
                    "receipt": .object(object)
                ])
            }

            let message: String
            if case let .string(resultMessage) = result {
                message = resultMessage
            } else {
                message = (try? result.jsonString()) ?? "Betaling kunne ikke gjennomføres."
            }
            return .object([
                "status": .string("quota_not_available"),
                "message": .string("Brukskvoten kunne ikke brukes: \(message)"),
                "resourceID": .string(resourceID),
                "topUpPath": .string("/chat-mvp?topup=1"),
                "policy": .object(await requesterPaymentPolicyObject(requester: requester))
            ])

        case "open_top_up":
            return .object([
                "status": .string("top_up_required"),
                "message": .string("Åpne top-up flyten. Ekstern betaling fyller bare ikke-overførbar brukskvote; PaymentGate trekker senere per handling."),
                "resourceID": .string(resourceID),
                "topUpPath": .string("/chat-mvp?topup=1"),
                "policy": .object(await requesterPaymentPolicyObject(requester: requester))
            ])

        case "change_policy":
            if case let .object(object) = payload,
               object.isEmpty == false,
               boolValue(object["showOnly"]) != true,
               let (gate, paymentRequester) = await paymentGateTarget(requester: requester),
               let identityDomain = await PaymentGateOwnerIdentitySupport.keyBoundIdentityDomain(for: requester) {
                var command = object
                command["identityDomain"] = .string(identityDomain)
                let result = try await gate.set(
                    keypath: "setUserPaymentPolicy",
                    value: .object(command),
                    requester: paymentRequester
                ) ?? .null
                return .object([
                    "status": .string("policy_update_attempted"),
                    "message": .string("Payment policy ble sendt til PaymentGate for lagring på brukerens identity."),
                    "result": result
                ])
            }

            return .object([
                "status": .string("policy_review"),
                "message": .string("Policy kan endres før spend: månedstak, maks per handling, lav-saldo-adferd, receipts/audit og tillatte rails. Auto-top-up holdes av i v0."),
                "resourceID": .string(resourceID),
                "policy": .object(await requesterPaymentPolicyObject(requester: requester))
            ])

        default:
            return .object([
                "status": .string("unsupported_payment_action"),
                "message": .string("Ukjent betalingshandling: \(mode)")
            ])
        }
    }

    private static func promptRequirementObject(requester: Identity) async throws -> Object? {
        guard let prompt = try await accessRequirementPromptCell(requester: requester) else {
            return nil
        }
        let state = try await prompt.get(keypath: "state", requester: requester)
        guard case let .object(stateObject) = state,
              case let .object(requirement)? = stateObject["requirement"] else {
            return nil
        }
        return requirement
    }

    private static func requesterPaymentPolicyObject(requester: Identity) async -> Object {
        let value = try? await requester.get(
            keypath: PaymentGatePolicy.identityRelativeKeypath(PaymentGatePolicy.entityUserPaymentPolicyKeypath),
            requester: requester
        )
        if case let .object(policy)? = value {
            return PaymentGatePolicy.normalizedUserPaymentPolicyObject(policy)
        }
        return PaymentGatePolicy.defaultUserPaymentPolicyObject()
    }

    private static func paymentQuoteObject(resourceID: String, requester: Identity) async -> Object {
        guard let (gate, gateOwner) = await paymentGateTarget(requester: requester),
              let quoteValue = try? await gate.get(keypath: "quote", requester: gateOwner),
              case let .object(quoteObject) = quoteValue else {
            return [
                "resourceID": .string(resourceID),
                "currency": .string(PaymentGatePolicy.currency),
                "priceMinorUnits": .integer(Int(clamping: PaymentGatePolicy.defaultPricesByResource[resourceID] ?? PaymentGatePolicy.defaultPriceMinorUnits)),
                "priceQuotaUnits": .integer(Int(clamping: PaymentGatePolicy.quotaUnits(forSettlementMinorUnits: PaymentGatePolicy.defaultPricesByResource[resourceID] ?? PaymentGatePolicy.defaultPriceMinorUnits))),
                "unitModel": .object(PaymentGatePolicy.unitModelObject())
            ]
        }

        if case let .list(resources)? = quoteObject["resources"] {
            for item in resources {
                guard case let .object(resourceObject) = item,
                      resourceObject["resourceID"]?.string == resourceID else {
                    continue
                }
                var object = resourceObject
                object["currency"] = quoteObject["currency"] ?? .string(PaymentGatePolicy.currency)
                object["unitModel"] = quoteObject["unitModel"] ?? .object(PaymentGatePolicy.unitModelObject())
                return object
            }
        }

        return quoteObject
    }

    private static func paymentQuoteSummary(resourceID: String, quote: Object) -> String {
        let minorUnits = intValue(quote["priceMinorUnits"]) ?? Int(clamping: PaymentGatePolicy.defaultPricesByResource[resourceID] ?? PaymentGatePolicy.defaultPriceMinorUnits)
        let quotaUnits = intValue(quote["priceQuotaUnits"]) ?? Int(clamping: PaymentGatePolicy.quotaUnits(forSettlementMinorUnits: UInt64(max(0, minorUnits))))
        let currency = quote["currency"]?.string ?? PaymentGatePolicy.currency
        return "Pris for `\(resourceID)`: \(minorUnits) minor units \(currency), \(quotaUnits) brukskvote-enheter."
    }

    private static func paymentGateTarget(requester: Identity) async -> (PaymentGateCell, Identity)? {
        guard let resolver = CellBase.defaultCellResolver,
              await PaymentGateOwnerIdentitySupport.keyBoundIdentityDomain(for: requester) != nil else {
            return nil
        }
        let lookupRequester = await scaffoldRequesterIdentity() ?? requester
        guard let gate = try? await resolver.cellAtEndpoint(
            endpoint: "cell:///PaymentGate",
            requester: lookupRequester
        ) as? PaymentGateCell else {
            return nil
        }
        return (gate, requester)
    }

    private static func scaffoldRequesterIdentity() async -> Identity? {
        guard let vault = CellBase.defaultIdentityVault else { return nil }
        for candidate in ["Scaffold", "scaffold", "private"] {
            if let identity = await vault.identity(for: candidate, makeNewIfNotFound: false) {
                return identity
            }
        }
        for candidate in ["Scaffold", "scaffold", "private"] {
            if let identity = await vault.identity(for: candidate, makeNewIfNotFound: true) {
                return identity
            }
        }
        return nil
    }

    private static func paymentResourceID(sourceCellEndpoint: String, proofKeypath: String?) -> String {
        let normalizedProofKeypath = proofKeypath?.lowercased() ?? ""
        for resourceID in PaymentGatePolicy.defaultPricesByResource.keys {
            if normalizedProofKeypath.contains(PaymentGatePolicy.normalizedResourceComponent(resourceID)) {
                return resourceID
            }
        }
        if sourceCellEndpoint == "cell:///PaymentProofDoor" {
            return PaymentGatePolicy.paymentProofDoorEntryResourceID
        }
        if sourceCellEndpoint == "cell:///Chat" {
            return PaymentGatePolicy.chatEntryResourceID
        }
        if sourceCellEndpoint == "cell:///Todo" {
            return PaymentGatePolicy.todoEntryResourceID
        }
        return "\(sourceCellEndpoint)#entry"
    }

    private static func stringValue(_ value: ValueType?) -> String? {
        guard case let .string(string)? = value else { return nil }
        return string
    }

    private static func intValue(_ value: ValueType?) -> Int? {
        switch value {
        case .integer(let integer)?:
            return integer
        case .number(let integer)?:
            return integer
        case .float(let double)?:
            return Int(double)
        case .string(let string)?:
            return Int(string.trimmingCharacters(in: .whitespacesAndNewlines))
        default:
            return nil
        }
    }

    private static func boolValue(_ value: ValueType?) -> Bool? {
        switch value {
        case .bool(let bool)?:
            return bool
        case .string(let string)?:
            switch string.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() {
            case "true", "1", "yes":
                return true
            case "false", "0", "no":
                return false
            default:
                return nil
            }
        default:
            return nil
        }
    }

    private static func preconfigureAccessRequirementPrompt(
        from requirement: BootstrapAccessRequirement,
        requester: Identity
    ) async {
        guard CellBase.defaultCellResolver != nil else { return }
        for attempt in 0..<2 {
            do {
                guard let prompt = try await accessRequirementPromptCell(
                    requester: requester,
                    recoverStaleOwner: attempt == 0
                ) else {
                    return
                }
                _ = try await prompt.set(
                    keypath: "loadRequirementDraft",
                    value: .object([
                        "subjectLabel": .string(requirement.subjectLabel),
                        "targetEndpoint": .string(requirement.sourceCellEndpoint),
                        "grantKeypath": .string(requirement.grantKeypath),
                        "grantPermission": .string(requirement.grantPermission),
                        "agreementName": .string(requirement.agreementName),
                        "purpose": .string(requirement.purpose),
                        "durationHours": .integer(requirement.durationHours),
                        "kind": .string(requirement.kind),
                        "proofKeypath": requirement.proofKeypath.map(ValueType.string) ?? .null,
                        "proofCredentialType": requirement.proofCredentialType.map(ValueType.string) ?? .null,
                        "proofPrompt": requirement.proofPrompt.map(ValueType.string) ?? .null,
                        "resolutionHint": requirement.resolutionHint.map(ValueType.string) ?? .null,
                        "resolutionRequesterUUID": requirement.resolutionRequesterUUID.map(ValueType.string) ?? .null,
                        "resolutionRequesterDisplayName": requirement.resolutionRequesterDisplayName.map(ValueType.string) ?? .null,
                        "decisionSummary": .string("Loaded from blocked skeleton reference `\(requirement.referenceLabel)`.")
                    ]),
                    requester: requester
                )
                return
            } catch {
                guard attempt == 0,
                      isIdentityReferenceMismatch(error),
                      await resetAccessRequirementPromptMapping(for: requester) else {
                    return
                }
            }
        }
    }

    private static let bootstrapMenuKeypaths = [
        "upperLeftMenu",
        "upperMidMenu",
        "upperRightMenu",
        "lowerLeftMenu",
        "lowerMidMenu",
        "lowerRightMenu"
    ]

    private static func bootstrapMenuSummaryObject() -> Object {
        var menusObject: Object = [:]
        for keypath in bootstrapMenuKeypaths {
            menusObject[keypath] = bootstrapMenuSummaryList(forMenuKeypath: keypath)
        }
        return menusObject
    }

    private static func bootstrapAvailableConfigurationSummaryList() -> ValueType {
        let configurations = bootstrapPublishedConfigurations(
            forMenuKeypath: ConfigurationCatalogClient.keypathAllConfigurations
        )
        return .list(configurations.map { .cellConfiguration(bootstrapConfigurationSummary(for: $0)) })
    }

    private static func bootstrapMenuSummaryList(
        forMenuKeypath keypath: String
    ) -> ValueType {
        let configurations = bootstrapPublishedConfigurations(forMenuKeypath: keypath)
        return .list(configurations.map { .cellConfiguration(bootstrapConfigurationSummary(for: $0)) })
    }

    private static func bootstrapPublishedConfigurations(
        forMenuKeypath keypath: String
    ) -> [CellConfiguration] {
        let catalogConfigurations: [CellConfiguration]
        if keypath == ConfigurationCatalogClient.keypathAllConfigurations {
            catalogConfigurations = ConfigurationCatalogCell.defaultCatalogConfigurations()
        } else {
            catalogConfigurations = ConfigurationCatalogCell.defaultCatalogConfigurations(forMenuKeypath: keypath)
        }

        return ConfigurationCatalogCell.portholePublishedConfigurations(from: catalogConfigurations)
    }

    private static func configurationWithDefaultChatWorkbench(_ configuration: CellConfiguration?) -> CellConfiguration? {
        guard let defaultChatConfiguration = defaultChatWorkbenchConfiguration(),
              let defaultChatSkeleton = defaultChatConfiguration.skeleton else {
            return configuration
        }

        guard var effectiveConfiguration = configuration else {
            return defaultChatConfiguration
        }

        guard shouldUseDefaultChatWorkbench(for: effectiveConfiguration) else {
            return effectiveConfiguration
        }

        effectiveConfiguration.skeleton = defaultChatSkeleton
        effectiveConfiguration.cellReferences = mergeDefaultChatReferences(
            defaultChatConfiguration.cellReferences ?? [],
            into: effectiveConfiguration.cellReferences ?? []
        )
        return effectiveConfiguration
    }

    private static func shouldUseDefaultChatWorkbench(for configuration: CellConfiguration) -> Bool {
        guard let skeleton = configuration.skeleton else {
            return true
        }

        if case let .Text(text) = skeleton {
            return text.text == "Hello HAVEN"
                && text.keypath == nil
                && text.url == nil
        }

        return isLegacyCoPilotChatResourceRouter(configuration)
    }

    private static func isLegacyCoPilotChatResourceRouter(_ configuration: CellConfiguration) -> Bool {
        guard isPersonalChatHubConfiguration(configuration),
              let skeleton = configuration.skeleton,
              let data = try? JSONEncoder().encode(skeleton),
              let json = String(data: data, encoding: .utf8) else {
            return false
        }
        return json.contains("chatHub.state.assistant.resourceMatches")
            && json.contains("Last inn flaten")
            && json.contains("actionKeypath")
    }

    private static func isPersonalChatHubConfiguration(_ configuration: CellConfiguration) -> Bool {
        let normalizedName = normalizedConfigurationIdentity(configuration.name)
        let normalizedEndpoint = normalizedConfigurationIdentity(configuration.discovery?.sourceCellEndpoint)
        return normalizedEndpoint == normalizedConfigurationIdentity(PersonalChatHubContract.endpoint)
            || normalizedName == normalizedConfigurationIdentity("Co-Pilot Chat")
            || normalizedName == normalizedConfigurationIdentity("Invite Chat")
    }

    private static func defaultChatWorkbenchConfiguration() -> CellConfiguration? {
        PersonalCopilotConfigurationFactory.configuration(for: PersonalChatHubContract.endpoint)
            ?? PersonalCopilotConfigurationFactory.catalogConfigurations().first { $0.name == "Co-Pilot Chat" }
            ?? PersonalCopilotConfigurationFactory.catalogConfigurations().first { $0.name == "Invite Chat" }
    }

    private static func mergeDefaultChatReferences(
        _ defaultReferences: [CellReference],
        into existingReferences: [CellReference]
    ) -> [CellReference] {
        var labels = Set<String>()
        var merged = [CellReference]()

        for reference in defaultReferences + existingReferences {
            guard labels.insert(reference.label).inserted else {
                continue
            }
            merged.append(reference)
        }

        return merged
    }

    private static func bootstrapConfigurationSummary(for configuration: CellConfiguration) -> CellConfiguration {
        var summary = CellConfiguration(name: configuration.name)
        summary.uuid = configuration.uuid
        summary.description = configuration.description
        summary.discovery = configuration.discovery
        summary.skeleton = nil
        summary.cellReferences = nil
        return summary
    }

    static func executeAction(
        controlCell: OrchestratorCell,
        sessionId: String,
        action: PortholeActionRequest,
        requester: Identity
    ) async throws -> ValueType {
        guard let keypath = action.resolvedKeypath else {
            throw Abort(.badRequest, reason: "Missing action keypath.")
        }
        return try await executeAction(
            controlCell: controlCell,
            sessionId: sessionId,
            keypath: keypath,
            payload: action.resolvedPayload,
            requester: requester
        )
    }

    static func executeAction(
        controlCell: OrchestratorCell,
        sessionId: String,
        keypath: String,
        payload: ValueType?,
        requester: Identity
    ) async throws -> ValueType {
        let trimmed = keypath.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else {
            throw Abort(.badRequest, reason: "Missing keypath.")
        }

        if trimmed == "chatHub.assistant.provider.register" {
            guard let payload else {
                throw Abort(.badRequest, reason: "Missing provider registration payload.")
            }
            let registeredProviderCount = await ChatScopedAIProviderRegistry.shared.register(
                requesterUUID: requester.uuid,
                payload: payload
            )
            return .object([
                "contractVersion": .string("porthole-web-v2"),
                "ok": .bool(true),
                "action": .string(trimmed),
                "result": .object([
                    "ok": .bool(true),
                    "status": .string("registered"),
                    "registeredProviderCount": .integer(registeredProviderCount),
                    "providerRecommendation": .null
                ])
            ])
        }

        if let editorActionResult = try await executeEditorActionIfNeeded(
            controlCell: controlCell,
            sessionId: sessionId,
            keypath: trimmed,
            payload: payload,
            requester: requester
        ) {
            return editorActionResult
        }

        let rawResult: ValueType

        if trimmed == "porthole.approveAccessRequirement" {
            rawResult = try await executeInlineAccessRequirementAction(
                sessionId: sessionId,
                promptActionKeypath: "approveRequest",
                requester: requester
            )
        } else if trimmed == "porthole.useExistingPaymentQuota" {
            rawResult = try await executePaymentRequirementAction(
                sessionId: sessionId,
                mode: "use_existing_quota",
                payload: payload ?? .bool(true),
                requester: requester
            )
        } else if trimmed == "porthole.openPaymentTopUp" {
            rawResult = try await executePaymentRequirementAction(
                sessionId: sessionId,
                mode: "open_top_up",
                payload: payload ?? .bool(true),
                requester: requester
            )
        } else if trimmed == "porthole.changePaymentPolicy" {
            rawResult = try await executePaymentRequirementAction(
                sessionId: sessionId,
                mode: "change_policy",
                payload: payload ?? .bool(true),
                requester: requester
            )
        } else if trimmed == "porthole.requestAccessRequirement" {
            rawResult = try await executeInlineAccessRequirementAction(
                sessionId: sessionId,
                promptActionKeypath: "requestExternalAccess",
                payload: payload ?? .bool(true),
                requester: requester
            )
        } else if trimmed == "porthole.submitAccessRequirementCredential" {
            rawResult = try await executeInlineAccessRequirementAction(
                sessionId: sessionId,
                promptActionKeypath: "submitCredential",
                payload: payload ?? .null,
                requester: requester
            )
        } else if trimmed == "porthole.denyAccessRequirement" {
            rawResult = try await executeInlineAccessRequirementAction(
                sessionId: sessionId,
                promptActionKeypath: "denyRequest",
                requester: requester
            )
        } else if trimmed == "addConfiguration" {
            guard let payload else { throw Abort(.badRequest, reason: "Missing addConfiguration payload.") }
            _ = try await loadRequestedConfiguration(
                from: payload,
                controlCell: controlCell,
                requester: requester
            )
            rawResult = .string("ok")
        } else if trimmed == "removeReference" {
            guard let label = extractLabel(from: payload), !label.isEmpty else {
                throw Abort(.badRequest, reason: "Missing label for removeReference.")
            }
            guard let configuration = controlCell.getCellConfiguration(),
                  let references = configuration.cellReferences,
                  let targetReference = references.first(where: { $0.label == label }) else {
                throw Abort(.notFound, reason: "Reference with label '\(label)' not found.")
            }
            try await controlCell.removeCellReference(targetReference, requester: requester)
            rawResult = .string("ok")
        } else if let separator = trimmed.firstIndex(of: ".") {
            let label = String(trimmed[..<separator])
            let nestedKeypath = String(trimmed[trimmed.index(after: separator)...])
            let referenceLookupRequester = await ownerRequester(for: controlCell, requester: requester)
            let configuration = configurationWithDefaultChatWorkbench(controlCell.getCellConfiguration())
            let declaredReference = actionReference(for: label, in: configuration)
            var target: ReferencedActionTarget?
            if !label.isEmpty && !nestedKeypath.isEmpty {
                target = await referencedActionTargetForAction(
                    controlCell: controlCell,
                    label: label,
                    requester: requester,
                    referenceLookupRequester: referenceLookupRequester
                )
                if target == nil && label == "chatHub",
                   let chatHubTarget = await referencedActionTarget(
                    controlCell: controlCell,
                    label: label,
                    requester: referenceLookupRequester
                   ) {
                    target = ReferencedActionTarget(cell: chatHubTarget, actionRequester: requester)
                }
            }
            if !label.isEmpty,
               !nestedKeypath.isEmpty,
               let target {
                do {
                    if let payload {
                        rawResult = try await setReferencedTarget(
                            target.cell,
                            nestedKeypath: nestedKeypath,
                            fullKeypath: trimmed,
                            payload: payload,
                            requester: target.actionRequester
                        )
                    } else {
                        rawResult = try await getReferencedTarget(
                            target.cell,
                            nestedKeypath: nestedKeypath,
                            fullKeypath: trimmed,
                            requester: target.actionRequester
                        )
                    }
                } catch {
                    if (isIdentityReferenceMismatch(error) || isNotFoundError(error)),
                       let recoveredTarget = await recoveredReferencedActionTargetForAction(
                        controlCell: controlCell,
                        label: label,
                        requester: requester,
                        referenceLookupRequester: referenceLookupRequester
                       ) {
                        if let payload {
                            rawResult = try await setReferencedTarget(
                                recoveredTarget.cell,
                                nestedKeypath: nestedKeypath,
                                fullKeypath: trimmed,
                                payload: payload,
                                requester: recoveredTarget.actionRequester
                            )
                        } else {
                            rawResult = try await getReferencedTarget(
                                recoveredTarget.cell,
                                nestedKeypath: nestedKeypath,
                                fullKeypath: trimmed,
                                requester: recoveredTarget.actionRequester
                            )
                        }
                        return try await finishActionEnvelope(
                            sessionId: sessionId,
                            actionKeypath: trimmed,
                            rawResult: rawResult,
                            controlCell: controlCell,
                            requester: requester
                        )
                    }
                    guard label == "chatHub",
                          target.cell is PersonalChatHubCell == false,
                          isNotFoundError(error),
                          let chatHubTarget = await inspectionTargetCell(
                            endpoint: PersonalChatHubContract.endpoint,
                            requester: requester
                          ) else {
                        throw error
                    }
                    if let payload {
                        rawResult = try await setReferencedTarget(
                            chatHubTarget,
                            nestedKeypath: nestedKeypath,
                            fullKeypath: trimmed,
                            payload: payload,
                            requester: requester
                        )
                    } else {
                        rawResult = try await getReferencedTarget(
                            chatHubTarget,
                            nestedKeypath: nestedKeypath,
                            fullKeypath: trimmed,
                            requester: requester
                        )
                    }
                }
            } else if declaredReference != nil {
                throw Abort(
                    .serviceUnavailable,
                    reason: "Referenced cell '\(label)' is not available for action '\(trimmed)'."
                )
            } else if let payload {
                rawResult = try await controlCell.set(keypath: trimmed, value: payload, requester: requester) ?? .null
            } else {
                rawResult = try await controlCell.get(keypath: trimmed, requester: requester)
            }
        } else if let payload {
            rawResult = try await controlCell.set(keypath: trimmed, value: payload, requester: requester) ?? .null
        } else {
            rawResult = try await controlCell.get(keypath: trimmed, requester: requester)
        }

        let storedCurrentConfiguration = controlCell.getCellConfiguration()
        let currentConfiguration: CellConfiguration?
        if let storedCurrentConfiguration {
            currentConfiguration = await EditableCellConfigurationOverlayResolver.overlay(
                configuration: storedCurrentConfiguration,
                requester: requester
            )
        } else {
            currentConfiguration = nil
        }
        let refreshEditableConfigurationState = trimmed == "addConfiguration"
        let editableConfigurationState = refreshEditableConfigurationState
            ? await currentEditableState(
                for: currentConfiguration,
                requester: requester
            )
            : nil
        let committedEditorBaseConfiguration = editorCommittedConfiguration(
            currentConfiguration: currentConfiguration,
            editableConfigurationState: editableConfigurationState
        )
        let committedEditorConfiguration = configurationWithDefaultChatWorkbench(
            committedEditorBaseConfiguration
        )
        let editorState = PortholeEditorSessionStore.shared.sync(
            sessionId: sessionId,
            committedConfiguration: committedEditorConfiguration,
            committedSourceRevision: editableConfigurationState?.revision
        )
        return makeActionEnvelope(
            actionKeypath: trimmed,
            result: rawResult,
            editorState: editorState,
            includeDocumentSnapshots: false,
            editableConfigurationState: editableConfigurationState
        )
    }

    private static func finishActionEnvelope(
        sessionId: String,
        actionKeypath: String,
        rawResult: ValueType,
        controlCell: OrchestratorCell,
        requester: Identity
    ) async throws -> ValueType {
        let storedCurrentConfiguration = controlCell.getCellConfiguration()
        let currentConfiguration: CellConfiguration?
        if let storedCurrentConfiguration {
            currentConfiguration = await EditableCellConfigurationOverlayResolver.overlay(
                configuration: storedCurrentConfiguration,
                requester: requester
            )
        } else {
            currentConfiguration = nil
        }
        let refreshEditableConfigurationState = actionKeypath == "addConfiguration"
        let editableConfigurationState = refreshEditableConfigurationState
            ? await currentEditableState(
                for: currentConfiguration,
                requester: requester
            )
            : nil
        let committedEditorBaseConfiguration = editorCommittedConfiguration(
            currentConfiguration: currentConfiguration,
            editableConfigurationState: editableConfigurationState
        )
        let committedEditorConfiguration = configurationWithDefaultChatWorkbench(
            committedEditorBaseConfiguration
        )
        let editorState = PortholeEditorSessionStore.shared.sync(
            sessionId: sessionId,
            committedConfiguration: committedEditorConfiguration,
            committedSourceRevision: editableConfigurationState?.revision
        )
        return makeActionEnvelope(
            actionKeypath: actionKeypath,
            result: rawResult,
            editorState: editorState,
            includeDocumentSnapshots: false,
            editableConfigurationState: editableConfigurationState
        )
    }

    private struct ReferencedActionTarget {
        let cell: Meddle
        let actionRequester: Identity
    }

    private static func referencedActionTargetForAction(
        controlCell: OrchestratorCell,
        label: String,
        requester: Identity,
        referenceLookupRequester: Identity
    ) async -> ReferencedActionTarget? {
        if label == "chatHub",
           let chatHub = await inspectionTargetCell(
            endpoint: PersonalChatHubContract.endpoint,
            requester: requester
           ) {
            return ReferencedActionTarget(cell: chatHub, actionRequester: requester)
        }

        let configuration = configurationWithDefaultChatWorkbench(controlCell.getCellConfiguration())
        let reference = actionReference(
            for: label,
            in: configuration
        )

        guard let reference else {
            if label == "chatHub",
               let chatHub = await inspectionTargetCell(
                endpoint: PersonalChatHubContract.endpoint,
                requester: requester
               ) {
                return ReferencedActionTarget(cell: chatHub, actionRequester: requester)
            }
            return nil
        }

        let resolvedReference = resolvedSharedWorkbenchReference(
            for: reference,
            label: label,
            configuration: configuration
        )
        let referenceResolutionRequester = await referenceResolutionRequester(
            for: resolvedReference,
            label: label,
            configuration: configuration,
            requester: requester,
            referenceLookupRequester: referenceLookupRequester
        )

        if isSharedWorkbenchConfiguration(configuration),
           isSharedWorkbenchOwnerTargetLabel(label),
           let target = await inspectionTargetCell(for: resolvedReference, requester: referenceResolutionRequester) {
            await ensurePortholeRuntimeBindingsIfNeeded(target, requester: referenceResolutionRequester)
            return ReferencedActionTarget(cell: target, actionRequester: requester)
        }

        if isRequesterScopedConferencePreviewReference(resolvedReference),
           let target = await inspectionTargetCell(for: resolvedReference, requester: referenceResolutionRequester) {
            await ensurePortholeRuntimeBindingsIfNeeded(target, requester: requester)
            return ReferencedActionTarget(cell: target, actionRequester: requester)
        }

        if isRequesterOwnedReference(resolvedReference, label: label),
           let target = await inspectionTargetCell(for: resolvedReference, requester: referenceResolutionRequester) {
            await ensurePortholeRuntimeBindingsIfNeeded(target, requester: requester)
            return ReferencedActionTarget(cell: target, actionRequester: requester)
        }

        if isEndpointScopedUtilityReference(resolvedReference),
           let target = await inspectionTargetCell(for: resolvedReference, requester: referenceResolutionRequester) {
            await ensurePortholeRuntimeBindingsIfNeeded(target, requester: requester)
            return ReferencedActionTarget(cell: target, actionRequester: requester)
        }

        if let attached = await controlCell.getEmitterWithLabel(label, requester: referenceLookupRequester) as? Meddle {
            // Resolution may require the control-cell owner, but dispatch must
            // preserve the proved browser identity. Using the referenced Cell
            // owner here turns renderer routing into an authorization bypass
            // and breaks requester-relative actions such as self top-up.
            await ensurePortholeRuntimeBindingsIfNeeded(attached, requester: requester)
            return ReferencedActionTarget(cell: attached, actionRequester: requester)
        }

        if let target = await inspectionTargetCell(for: resolvedReference, requester: referenceResolutionRequester) {
            await ensurePortholeRuntimeBindingsIfNeeded(target, requester: requester)
            return ReferencedActionTarget(cell: target, actionRequester: requester)
        }

        if label == "chatHub",
           let chatHub = await inspectionTargetCell(
            endpoint: PersonalChatHubContract.endpoint,
            requester: requester
           ) {
            return ReferencedActionTarget(cell: chatHub, actionRequester: requester)
        }
        return nil
    }

    private static func actionReference(
        for label: String,
        in configuration: CellConfiguration?
    ) -> CellReference? {
        let normalizedLabel = label
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        if let reference = configuration?.cellReferences?.first(where: {
            $0.label.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() == normalizedLabel
        }) {
            return reference
        }

        guard normalizedLabel == "workbenchaccess" else {
            return nil
        }
        return CellReference(endpoint: WorkbenchAccessGrantCell.endpoint, label: "workbenchAccess")
    }

    private static func isWorkbenchAccessGrantConfiguration(_ configuration: CellConfiguration?) -> Bool {
        guard let configuration else { return false }
        let normalizedName = configuration.name
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        let normalizedEndpoint = configuration.discovery?.sourceCellEndpoint?
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        let normalizedSourceName = configuration.discovery?.sourceCellName?
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        return normalizedEndpoint == WorkbenchAccessGrantCell.endpoint.lowercased()
            || normalizedSourceName == "workbenchaccessgrantcell"
            || normalizedName == "workbench access grant"
    }

    @discardableResult
    static func resetStaleWorkbenchAccessGrantSharedMappingIfNeeded(
        requester: Identity
    ) async -> Bool {
        guard let resolver = CellBase.defaultCellResolver else {
            return false
        }
        var namedCells = await resolver.namedCells(requester: requester)
        guard namedCells.removeValue(forKey: "WorkbenchAccessGrant") != nil else {
            return false
        }
        await resolver.setNamedCells(namedCells, requester: requester)
        CellBase.diagnosticLog(
            "Removed unavailable WorkbenchAccessGrant shared resolver mapping before retry",
            domain: .resolver
        )
        return true
    }

    private static func isPersistedCellUnavailable(_ error: Error) -> Bool {
        if case CellSetupError.persistedCellUnavailable = error {
            return true
        }
        return false
    }

    private static func recoveredReferencedActionTargetForAction(
        controlCell: OrchestratorCell,
        label: String,
        requester: Identity,
        referenceLookupRequester: Identity
    ) async -> ReferencedActionTarget? {
        let configuration = configurationWithDefaultChatWorkbench(controlCell.getCellConfiguration())
        guard let reference = actionReference(for: label, in: configuration) else {
            return nil
        }
        let didReset = await ConferencePreviewWrapperResolverSupport.resetStalePreviewMappingsIfNeeded(
            for: reference.endpoint,
            requester: requester
        )
        guard didReset else {
            return nil
        }
        if reference.endpoint.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() == "cell:///conferenceadminpreviewshell" {
            try? await ConferenceAdminPreviewAccessSupport.ensurePreviewAccess(
                for: requester
            )
        }
        return await referencedActionTargetForAction(
            controlCell: controlCell,
            label: label,
            requester: requester,
            referenceLookupRequester: referenceLookupRequester
        )
    }

    private static func isEndpointScopedUtilityReference(_ reference: CellReference) -> Bool {
        let normalizedEndpoint = reference.endpoint
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        return normalizedEndpoint == "cell:///mermaidrenderer"
            || normalizedEndpoint == "cell:///markdownrenderer"
            || normalizedEndpoint == WorkbenchAccessGrantCell.endpoint.lowercased()
    }

    private static func isRequesterOwnedReference(_ reference: CellReference, label: String) -> Bool {
        let normalizedLabel = label
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        let normalizedEndpoint = reference.endpoint
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()

        let requesterOwnedLabels: Set<String> = [
            "arendalsukaparticipant",
            "workitems",
            "projectportfolio",
            "ownersetup",
            "ideaworkspace",
            "todo",
            "graph",
            "githubsync"
        ]
        if requesterOwnedLabels.contains(normalizedLabel) {
            return true
        }

        return [
            ArendalsukaParticipantProgramContract.endpoint.lowercased(),
            "cell:///workitem",
            "cell:///projectportfolio",
            "cell:///workbenchownersetup",
            "cell:///ideataskworkspace",
            "cell:///todo",
            "cell:///graphstore",
            "cell:///githubworksync"
        ].contains(normalizedEndpoint)
    }

    private static func shouldRedactProjectedStateForRequester(reference: CellReference) -> Bool {
        isEndpointScopedUtilityReference(reference) == false
    }

    private static func attachedReferenceRequester(
        for target: Meddle,
        label: String,
        configuration: CellConfiguration?,
        requester: Identity,
        referenceLookupRequester: Identity
    ) async -> Identity {
        if label == "chatHub" {
            return requester
        }
        if target is WorkbenchAccessGrantCell {
            return requester
        }
        if isSharedWorkbenchConfiguration(configuration),
           isSharedWorkbenchOwnerTargetLabel(label) {
            return requester
        }
        if label == "scaffoldSetup" || target is ScaffoldSetupCell {
            return requester
        }
        if let generalCell = target as? GeneralCell {
            return await ownerRequester(for: generalCell, requester: referenceLookupRequester)
        }
        return referenceLookupRequester
    }

    private static func isSharedWorkbenchConfiguration(_ configuration: CellConfiguration?) -> Bool {
        guard let configuration else { return false }
        let normalizedName = configuration.name
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        let normalizedUUID = configuration.uuid
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        return normalizedName == WorkbenchAccessGrantCell.sharedWorkbenchConfigurationName.lowercased()
            || normalizedUUID.hasPrefix("shared-workbench-")
    }

    private static func isSharedWorkbenchOwnerTargetLabel(_ label: String) -> Bool {
        [
            "workitems",
            "projectportfolio",
            "ownersetup",
            "githubsync",
            "ideaworkspace",
            "todo",
            "graph"
        ].contains(label.trimmingCharacters(in: .whitespacesAndNewlines).lowercased())
    }

    private static func resolvedSharedWorkbenchReference(
        for reference: CellReference,
        label: String,
        configuration: CellConfiguration?
    ) -> CellReference {
        guard isSharedWorkbenchConfiguration(configuration),
              isSharedWorkbenchOwnerTargetLabel(label) else {
            return reference
        }
        return WorkbenchAccessGrantCell.sharedWorkbenchConcreteReference(
            for: reference,
            in: configuration,
            label: label
        )
    }

    private static func referenceResolutionRequester(
        for reference: CellReference,
        label: String,
        configuration: CellConfiguration?,
        requester: Identity,
        referenceLookupRequester: Identity
    ) async -> Identity {
        if label == "chatHub" {
            return requester
        }
        if isSharedWorkbenchConfiguration(configuration),
           isSharedWorkbenchOwnerTargetLabel(label),
           let sharedTargetOwner = await WorkbenchAccessGrantCell.sharedWorkbenchTargetLookupRequester(
            configuration: configuration,
            label: label,
            endpoint: reference.endpoint,
            requester: requester
           ) {
            return sharedTargetOwner
        }
        if isSharedWorkbenchConfiguration(configuration),
           isSharedWorkbenchOwnerTargetLabel(label),
           WorkbenchAccessGrantCell.sharedWorkbenchConcreteEndpoint(
            in: configuration,
            label: label,
            sourceEndpoint: nil
           ) != nil {
            return requester
        }
        if isRequesterScopedConferencePreviewReference(reference) {
            return requester
        }
        if isEndpointScopedUtilityReference(reference) {
            return await scaffoldUtilityRequester(
                for: reference,
                fallback: referenceLookupRequester,
                identityUniqueRequester: requester
            )
        }
        if isRequesterOwnedReference(reference, label: label) {
            return requester
        }
        if let resolverScopedRequester = await resolverScopedReferenceRequester(
            for: reference,
            identityUniqueRequester: requester
        ) {
            return resolverScopedRequester
        }
        return referenceLookupRequester
    }


    private static func scaffoldUtilityRequester(
        for reference: CellReference,
        fallback: Identity,
        identityUniqueRequester: Identity
    ) async -> Identity {
        if let resolveOwner = await resolverScopedReferenceRequester(
            for: reference,
            identityUniqueRequester: identityUniqueRequester
        ),
           await identityIsBoundToAttachedHomeVault(resolveOwner) {
            return resolveOwner
        }

        if let configuredScaffoldUtilityRequester = await hydratedScaffoldUtilityRequester(),
           await identityIsBoundToAttachedHomeVault(configuredScaffoldUtilityRequester) {
            return configuredScaffoldUtilityRequester
        }

        return fallback
    }

    private static func resolverScopedReferenceRequester(
        for reference: CellReference,
        identityUniqueRequester: Identity
    ) async -> Identity? {
        guard let resolver = CellBase.defaultCellResolver else {
            return nil
        }
        let normalizedName = resolverName(forEndpoint: reference.endpoint)
        let snapshot = await resolver.resolverRegistrySnapshot(requester: Identity())
        guard let resolve = snapshot.resolves.first(where: {
            resolverName(forEndpoint: $0.name).caseInsensitiveCompare(normalizedName) == .orderedSame
        }) else {
            return nil
        }
        switch resolve.cellScope {
        case .identityUnique:
            return identityUniqueRequester
        case .scaffoldUnique:
            guard let vault = CellBase.defaultIdentityVault,
                  let owner = await vault.identity(for: resolve.identityDomain, makeNewIfNotFound: false),
                  await identityIsBoundToAttachedHomeVault(owner) else {
                return nil
            }
            return owner
        case .template:
            return nil
        }
    }

    private static func hydratedScaffoldUtilityRequester() async -> Identity? {
        guard let configuredScaffoldUtilityRequester else {
            return nil
        }
        guard await identityIsBoundToAttachedHomeVault(configuredScaffoldUtilityRequester) else {
            return nil
        }
        return configuredScaffoldUtilityRequester
    }

    private static func resolverName(forEndpoint endpoint: String) -> String {
        let trimmed = endpoint.trimmingCharacters(in: .whitespacesAndNewlines)
        let prefix = "cell:///"
        if trimmed.lowercased().hasPrefix(prefix) {
            return String(trimmed.dropFirst(prefix.count))
        }
        return trimmed
    }

    private static func identityIsBoundToAttachedHomeVault(_ identity: Identity) async -> Bool {
        guard let homeVaultReference = identity.homeVaultReference,
              homeVaultReference.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty == false else {
            return false
        }
        guard let vault = identity.identityVault,
              let attachedVaultReference = await vault.identityVaultReference(),
              identity.signingPublicKeyFingerprint != nil else {
            return false
        }
        guard attachedVaultReference == homeVaultReference else {
            return false
        }
        return await vault.identityExistInVault(identity)
    }

    private static func isRequesterScopedConferencePreviewReference(_ reference: CellReference) -> Bool {
        let normalizedEndpoint = reference.endpoint
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        return requesterScopedConferencePreviewEndpoints.contains(normalizedEndpoint)
    }

    private static let requesterScopedConferencePreviewEndpoints: Set<String> = [
        "cell:///conferenceparticipantpreviewshell",
        "cell:///conferenceaigatewaypreview",
        "cell:///conferencepublicprofilepreview",
        "cell:///conferencepublicprofileeditorpreview",
        "cell:///conferenceadminpreviewshell",
        "cell:///conferencesponsorpreviewshell"
    ]

    private static func referencedActionTarget(
        controlCell: OrchestratorCell,
        label: String,
        requester: Identity
    ) async -> Meddle? {
        if label == "chatHub",
           let chatHub = await inspectionTargetCell(
            endpoint: PersonalChatHubContract.endpoint,
            requester: requester
           ) {
            return chatHub
        }
        let configuration = configurationWithDefaultChatWorkbench(controlCell.getCellConfiguration())
        guard let reference = configuration?.cellReferences?.first(where: { $0.label == label }) else {
            if label == "chatHub" {
                return await inspectionTargetCell(
                    endpoint: PersonalChatHubContract.endpoint,
                    requester: requester
                )
            }
            return nil
        }
        let resolvedReference = resolvedSharedWorkbenchReference(
            for: reference,
            label: label,
            configuration: configuration
        )
        if isEndpointScopedUtilityReference(resolvedReference),
           let target = await inspectionTargetCell(for: resolvedReference, requester: requester) {
            await ensurePortholeRuntimeBindingsIfNeeded(target, requester: requester)
            return target
        }
        if let attached = await controlCell.getEmitterWithLabel(label, requester: requester) as? Meddle {
            await ensurePortholeRuntimeBindingsIfNeeded(attached, requester: requester)
            return attached
        }
        if let target = await inspectionTargetCell(for: resolvedReference, requester: requester) {
            await ensurePortholeRuntimeBindingsIfNeeded(target, requester: requester)
            return target
        }
        if label == "chatHub" {
            return await inspectionTargetCell(
                endpoint: PersonalChatHubContract.endpoint,
                requester: requester
            )
        }
        return nil
    }

    private static func setReferencedTarget(
        _ target: Meddle,
        nestedKeypath: String,
        fullKeypath: String,
        payload: ValueType,
        requester: Identity
    ) async throws -> ValueType {
        do {
            return try await target.set(keypath: nestedKeypath, value: payload, requester: requester) ?? .null
        } catch {
            guard isNotFoundError(error) else { throw error }
            return try await target.set(keypath: fullKeypath, value: payload, requester: requester) ?? .null
        }
    }

    private static func getReferencedTarget(
        _ target: Meddle,
        nestedKeypath: String,
        fullKeypath: String,
        requester: Identity
    ) async throws -> ValueType {
        do {
            return try await target.get(keypath: nestedKeypath, requester: requester)
        } catch {
            guard isNotFoundError(error) else { throw error }
            return try await target.get(keypath: fullKeypath, requester: requester)
        }
    }

    private static func isNotFoundError(_ error: Error) -> Bool {
        String(describing: error).localizedCaseInsensitiveContains("notFound")
    }

    private static func executeInlineAccessRequirementAction(
        sessionId: String,
        promptActionKeypath: String,
        payload: ValueType? = nil,
        requester: Identity
    ) async throws -> ValueType {
        guard let prompt = try await accessRequirementPromptCell(requester: requester) else {
            return .string("No access requirement is available right now.")
        }

        let promptStateBefore = try? await prompt.get(keypath: "state", requester: requester)
        let fingerprint = accessRequirementFingerprint(fromPromptState: promptStateBefore)
        guard let activeFingerprint = await accessRequirementDecisionStore.activeFingerprint(sessionId: sessionId),
              fingerprint == activeFingerprint else {
            return .string("No access requirement is available right now.")
        }

        if promptActionKeypath == "approveRequest", let fingerprint {
            await accessRequirementDecisionStore.clearDismissal(fingerprint, sessionId: sessionId)
        }

        let result = try await prompt.set(
            keypath: promptActionKeypath,
            value: payload ?? .bool(true),
            requester: requester
        ) ?? .null

        if promptActionKeypath == "denyRequest", let fingerprint {
            await accessRequirementDecisionStore.dismiss(fingerprint, sessionId: sessionId)
            return .string("Access request dismissed for this session.")
        }

        if let decisionSummary = accessRequirementDecisionSummary(fromPromptState: result) {
            return .string(decisionSummary)
        }
        return .string("Access request processed.")
    }

    private static func accessRequirementPromptCell(
        requester: Identity,
        recoverStaleOwner: Bool = true
    ) async throws -> Meddle? {
        guard let resolver = CellBase.defaultCellResolver else { return nil }
        guard let prompt = try await resolver.cellAtEndpoint(
            endpoint: accessRequirementPromptEndpoint,
            requester: requester
        ) as? Meddle else {
            return nil
        }

        await ensurePortholeRuntimeBindingsIfNeeded(prompt, requester: requester)

        guard recoverStaleOwner else { return prompt }
        do {
            _ = try await prompt.get(keypath: "state", requester: requester)
            return prompt
        } catch {
            guard isIdentityReferenceMismatch(error),
                  await resetAccessRequirementPromptMapping(for: requester) else {
                return prompt
            }
            guard let recoveredPrompt = try await resolver.cellAtEndpoint(
                endpoint: accessRequirementPromptEndpoint,
                requester: requester
            ) as? Meddle else {
                return nil
            }
            await ensurePortholeRuntimeBindingsIfNeeded(recoveredPrompt, requester: requester)
            return recoveredPrompt
        }
    }

    private static func isIdentityReferenceMismatch(_ error: Error) -> Bool {
        isIdentityReferenceMismatchDescription(String(describing: error))
    }

    private static func isIdentityReferenceMismatchDescription(_ description: String) -> Bool {
        let description = description.lowercased()
        return description.contains("deniedidentityreferencemismatch")
            || description.contains("identity_public_key_mismatch")
            || description.contains("public signing key did not match")
            || description.contains("failed to prove ownership")
    }

    @discardableResult
    private static func resetAccessRequirementPromptMapping(for requester: Identity) async -> Bool {
        guard let resolver = CellBase.defaultCellResolver else { return false }
        var identityNamedCells = await resolver.identityNamedCells(requester: requester)
        guard var requesterMappings = identityNamedCells[requester.uuid],
              requesterMappings[accessRequirementPromptReferenceName] != nil else {
            return false
        }
        requesterMappings[accessRequirementPromptReferenceName] = nil
        if requesterMappings.isEmpty {
            identityNamedCells[requester.uuid] = nil
        } else {
            identityNamedCells[requester.uuid] = requesterMappings
        }
        await resolver.setIdentityNamedCells(identityNamedCells, requester: requester)
        return true
    }

    private static func accessRequirementFingerprint(fromPromptState value: ValueType?) -> String? {
        guard case let .object(state)? = value,
              case let .object(requirement)? = state["requirement"],
              let direct = requirement["fingerprint"]?.string,
              direct.isEmpty == false else {
            return nil
        }
        return direct
    }

    private static func accessRequirementDecisionSummary(fromPromptState value: ValueType?) -> String? {
        guard case let .object(state)? = value,
              let summary = state["decisionSummary"]?.string,
              summary.isEmpty == false else {
            return nil
        }
        return summary
    }

    static func responseEnvelope(requestId: String?, payload: ValueType) -> PortholeWebSocketServerEnvelope {
        PortholeWebSocketServerEnvelope(
            kind: "response",
            requestId: requestId,
            payload: payload,
            message: nil,
            ok: true
        )
    }

    static func errorEnvelope(requestId: String?, error: Error) -> PortholeWebSocketServerEnvelope {
        let message: String
        if let abort = error as? AbortError {
            message = abort.reason
        } else {
            message = error.localizedDescription
        }
        return PortholeWebSocketServerEnvelope(
            kind: "error",
            requestId: requestId,
            payload: nil,
            message: message,
            ok: false
        )
    }

    private static func resolveRequestedCellConfiguration(
        from payload: ValueType,
        controlCell: OrchestratorCell,
        requester: Identity
    ) async throws -> CellConfiguration? {
        let effectivePayload: ValueType
        if ScaffoldLaunchRegistryPayloadSupport.launchSurfaceID(from: payload) != nil {
            guard let resolvedLaunchPayload = await resolveRuntimeSurfaceLaunch(
                payload,
                requester: requester
            ) else {
                return nil
            }
            effectivePayload = resolvedLaunchPayload
        } else {
            effectivePayload = payload
        }

        if let currentConfiguration = controlCell.getCellConfiguration(),
           payloadRequestsConfiguration(effectivePayload, matching: currentConfiguration) {
            return await EditableCellConfigurationOverlayResolver.overlay(
                configuration: currentConfiguration,
                requester: requester
            )
        }

        let directConfiguration = PortholeWebPayloads.decodeCellConfiguration(from: effectivePayload)
        if let configuration = directConfiguration,
           ConfigurationCatalogCell.isPortholePublishedConfiguration(configuration),
           configurationCarriesRenderableBody(configuration) {
            return configuration
        }

        let candidates = await availableCellConfigurations(
            for: controlCell,
            requester: requester,
            includeDefaultCatalog: false
        )

        if let configuration = directConfiguration {
            if let replacement = preferredPortholePublishedConfiguration(
                matching: configuration,
                in: candidates
            ) {
                return replacement
            }

            let defaultCandidates = defaultPortholePublishedConfigurations()
            if let replacement = preferredPortholePublishedConfiguration(
                matching: configuration,
                in: defaultCandidates
            ) {
                return replacement
            }
            if ConfigurationCatalogCell.isPortholePublishedConfiguration(configuration) {
                return configuration
            }
            return configuration
        }

        if let resolved = PortholeWebPayloads.resolveCellConfiguration(from: effectivePayload, candidates: candidates) {
            return preferredPortholePublishedConfiguration(matching: resolved, in: candidates) ?? resolved
        }

        let defaultCandidates = defaultPortholePublishedConfigurations()
        if let resolved = PortholeWebPayloads.resolveCellConfiguration(from: effectivePayload, candidates: defaultCandidates) {
            return preferredPortholePublishedConfiguration(matching: resolved, in: defaultCandidates) ?? resolved
        }
        return nil
    }

    private static func resolveRuntimeSurfaceLaunch(
        _ payload: ValueType,
        requester: Identity
    ) async -> ValueType? {
        guard let resolver = CellBase.defaultCellResolver,
              let registry = try? await resolver.cellAtEndpoint(
                endpoint: ScaffoldLaunchRegistryContract.endpoint,
                requester: requester
              ) as? Meddle else {
            return nil
        }
        await ensurePortholeRuntimeBindingsIfNeeded(registry, requester: requester)
        guard let routes = try? await registry.get(
            keypath: ScaffoldLaunchRegistryContract.publishedRoutesKeypath,
            requester: requester
        ) else {
            return nil
        }
        return ScaffoldLaunchRegistryPayloadSupport.resolveLaunchPayload(
            payload,
            routesValue: routes
        )
    }

    private static func repairedActiveConfigurationIfNeeded(
        _ activeConfiguration: CellConfiguration?,
        controlCell: OrchestratorCell,
        requester: Identity,
        loadRequester: Identity
    ) async -> CellConfiguration? {
        guard let activeConfiguration else { return nil }

        let candidates = defaultPortholePublishedConfigurations()
        guard let replacement = preferredPortholePublishedConfiguration(
            matching: activeConfiguration,
            in: candidates
        ), activeConfigurationNeedsPublishedRepair(activeConfiguration, replacement: replacement) else {
            return activeConfiguration
        }

        let sourceBackedConfiguration = await EditableCellConfigurationOverlayResolver.overlay(
            configuration: replacement,
            requester: requester
        )
        let loadConfiguration = portholeWebLoadConfiguration(sourceBackedConfiguration)
        do {
            try await loadPortholeConfiguration(
                loadConfiguration,
                controlCell: controlCell,
                requester: loadRequester
            )
            return loadConfiguration
        } catch {
            print("Porthole failed repairing active configuration '\(activeConfiguration.name)' from \(replacement.discovery?.sourceCellEndpoint ?? "unknown endpoint"): \(error)")
            return activeConfiguration
        }
    }

    private static func loadPortholeConfiguration(
        _ configuration: CellConfiguration,
        controlCell: OrchestratorCell,
        requester: Identity,
        referenceRequestersByLabel: [String: Identity] = [:]
    ) async throws {
        for reference in configuration.cellReferences ?? []
        where reference.endpoint == ArendalsukaAtlasImportAccessContract.resourceEndpoint {
            _ = try await ArendalsukaCanonicalAtlasResolution.resolve(
                requester: referenceRequestersByLabel[reference.label] ?? requester
            )
        }
        let previousLabels = Set(
            controlCell.getCellConfiguration()?.cellReferences?.map(\.label) ?? []
        )
        let nextLabels = Set(configuration.cellReferences?.map(\.label) ?? [])
        let transitionLabels = previousLabels.union(nextLabels)
        guard await controlCell.replacePortholeSessionFlowAccess(
            requester: requester,
            allowedLabels: transitionLabels,
            additionalRequestersByLabel: referenceRequestersByLabel
        ) else {
            throw Abort(
                .unauthorized,
                reason: "Porthole configuration loading requires a proof-bearing requester in its attached home vault."
            )
        }

        do {
            if referenceRequestersByLabel.isEmpty == false {
                try await controlCell.loadCellConfiguration(
                    configuration,
                    requester: requester,
                    referenceRequestersByLabel: referenceRequestersByLabel
                )
            } else {
                try await controlCell.loadCellConfiguration(configuration, requester: requester)
            }
        } catch {
            await controlCell.clearPortholeSessionFlowAccess()
            throw error
        }

        await controlCell.clearPortholeSessionFlowAccess()
    }

    private static func activeConfigurationNeedsPublishedRepair(
        _ active: CellConfiguration,
        replacement: CellConfiguration
    ) -> Bool {
        if active.skeleton == nil, replacement.skeleton != nil {
            return true
        }

        let activeEndpoint = normalizedLoadToken(active.discovery?.sourceCellEndpoint)
        let replacementEndpoint = normalizedLoadToken(replacement.discovery?.sourceCellEndpoint)
        if activeEndpoint.isEmpty, replacementEndpoint.isEmpty == false {
            return true
        }

        let activeReferences = Set((active.cellReferences ?? []).map(referenceIdentity))
        let replacementReferences = Set((replacement.cellReferences ?? []).map(referenceIdentity))
        if replacementReferences.isEmpty == false,
           replacementReferences.isSubset(of: activeReferences) == false {
            return true
        }

        return false
    }

    private static func referenceIdentity(_ reference: CellReference) -> String {
        "\(normalizedLoadToken(reference.label))::\(normalizedLoadToken(reference.endpoint))"
    }

    private static func defaultPortholePublishedConfigurations() -> [CellConfiguration] {
        ConfigurationCatalogCell.portholePublishedConfigurations(
            from: ConfigurationCatalogCell.defaultCatalogConfigurations()
        )
    }

    private static func availableCellConfigurations(
        for controlCell: OrchestratorCell,
        requester: Identity,
        includeDefaultCatalog: Bool = true
    ) async -> [CellConfiguration] {
        var collected = [CellConfiguration]()
        var seen = Set<String>()

        func append(_ configurations: [CellConfiguration]) {
            for configuration in configurations {
                let endpoint = configuration.discovery?.sourceCellEndpoint?.lowercased() ?? ""
                let identity = "\(configuration.uuid.lowercased())::\(configuration.name.lowercased())::\(endpoint)"
                if seen.insert(identity).inserted {
                    collected.append(configuration)
                }
            }
        }

        append(await WorkbenchAccessGrantCell.requesterSharedConfigurations(for: requester))

        if let availableValue = try? await controlCell.get(
            keypath: "availableCellConfigurations",
            requester: requester
        ) {
            append(ConfigurationCatalogClient.decodeConfigurations(from: availableValue))
        }

        let menuKeypaths = [
            "upperLeftMenu",
            "upperMidMenu",
            "upperRightMenu",
            "lowerLeftMenu",
            "lowerMidMenu",
            "lowerRightMenu"
        ]
        for keypath in menuKeypaths {
            guard let menuValue = try? await controlCell.get(
                keypath: keypath,
                requester: requester
            ) else {
                continue
            }
            append(ConfigurationCatalogClient.decodeConfigurations(from: menuValue))
        }

        if includeDefaultCatalog {
            let defaultConfigurations = ConfigurationCatalogCell.defaultCatalogConfigurations()
            append(defaultConfigurations)
        }

        return collected
    }

    private static func configurationCarriesRenderableBody(_ configuration: CellConfiguration) -> Bool {
        configuration.skeleton != nil || configuration.cellReferences?.isEmpty == false
    }

    private static func preferredPortholePublishedConfiguration(
        matching configuration: CellConfiguration,
        in candidates: [CellConfiguration]
    ) -> CellConfiguration? {
        let targetName = configuration.name.trimmingCharacters(in: .whitespacesAndNewlines)
        guard targetName.isEmpty == false else { return nil }
        let targetEndpoint = configuration.discovery?.sourceCellEndpoint?
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()

        return candidates.first { candidate in
            guard candidate.name.caseInsensitiveCompare(targetName) == .orderedSame,
                  ConfigurationCatalogCell.isPortholePublishedConfiguration(candidate) else {
                return false
            }
            guard let targetEndpoint else { return true }
            return candidate.discovery?.sourceCellEndpoint?
                .trimmingCharacters(in: .whitespacesAndNewlines)
                .lowercased() == targetEndpoint
        }
    }

    private static func payloadRequestsConfiguration(
        _ payload: ValueType,
        matching configuration: CellConfiguration
    ) -> Bool {
        if let direct = PortholeWebPayloads.decodeCellConfiguration(from: payload),
           configurationsShareLoadIdentity(direct, configuration) {
            return true
        }

        guard let lookup = PortholeWebPayloads.decodeCellConfigurationLookup(from: payload),
              lookup.hasIdentity else {
            return false
        }

        if let uuid = lookup.uuid,
           normalizedLoadToken(uuid) == normalizedLoadToken(configuration.uuid) {
            return true
        }

        if let name = lookup.name,
           normalizedLoadToken(name) == normalizedLoadToken(configuration.name) {
            guard let endpoint = lookup.sourceCellEndpoint else {
                return true
            }
            return normalizedLoadToken(endpoint) == normalizedLoadToken(configuration.discovery?.sourceCellEndpoint)
        }

        return false
    }

    private static func configurationsShareLoadIdentity(
        _ lhs: CellConfiguration,
        _ rhs: CellConfiguration
    ) -> Bool {
        if normalizedLoadToken(lhs.uuid) == normalizedLoadToken(rhs.uuid) {
            return true
        }
        guard normalizedLoadToken(lhs.name) == normalizedLoadToken(rhs.name) else {
            return false
        }
        let lhsEndpoint = normalizedLoadToken(lhs.discovery?.sourceCellEndpoint)
        let rhsEndpoint = normalizedLoadToken(rhs.discovery?.sourceCellEndpoint)
        return lhsEndpoint.isEmpty || rhsEndpoint.isEmpty || lhsEndpoint == rhsEndpoint
    }

    private static func normalizedLoadToken(_ value: String?) -> String {
        value?
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased() ?? ""
    }

    private static func portholeWebLoadConfiguration(_ configuration: CellConfiguration) -> CellConfiguration {
        var sanitized = configuration
        sanitized.cellReferences = configuration.cellReferences?.map(disableFeedSubscriptions)
        return sanitized
    }

    @discardableResult
    static func waitForLoadedReferenceState(
        _ configuration: CellConfiguration,
        controlCell: OrchestratorCell,
        requester: Identity
    ) async -> PortholeLoadedReferenceReadiness {
        let effectiveConfiguration = configurationWithDefaultChatWorkbench(configuration)
        let projectedKeypathsByLabel = PortholeBootstrapProjection.readableReferenceKeypaths(for: effectiveConfiguration)
        let references = effectiveConfiguration?.cellReferences ?? []
        let labelsRequiringState = references.compactMap { reference -> String? in
            let projectedKeypaths = projectedKeypathsByLabel[reference.label] ?? []
            let needsState = projectedKeypaths.contains { keypath in
                keypath == "state" || keypath.hasPrefix("state.")
            }
            return needsState ? reference.label : nil
        }

        guard labelsRequiringState.isEmpty == false else {
            return PortholeLoadedReferenceReadiness(
                readyLabels: [],
                accessGatedLabels: [:],
                unavailableLabels: [],
                unresolvedLabels: []
            )
        }

        let referenceLookupRequester = await ownerRequester(for: controlCell, requester: requester)
        var readyLabels = [String]()
        var accessGatedLabels = [String: String]()
        var unavailableLabels = [String]()
        var unresolvedLabels = [String]()
        for label in labelsRequiringState {
            guard let target = await referencedActionTargetForAction(
                controlCell: controlCell,
                label: label,
                requester: requester,
                referenceLookupRequester: referenceLookupRequester
            ) else {
                unresolvedLabels.append(label)
                continue
            }

            // Target resolution above awaits the explicit runtime-binding
            // readiness contract. A read that is still unavailable afterwards
            // is terminal for this load; blind polling only delays the surface
            // and cannot establish a missing lifecycle contract.
            switch await readLoadedReferenceState(
                target.cell,
                label: label,
                requester: requester
            ) {
            case .value:
                readyLabels.append(label)
            case .accessDenied(let reason):
                accessGatedLabels[label] = reason
            case .unavailable:
                unavailableLabels.append(label)
            }
        }

        let readiness = PortholeLoadedReferenceReadiness(
            readyLabels: readyLabels.sorted(),
            accessGatedLabels: accessGatedLabels,
            unavailableLabels: unavailableLabels.sorted(),
            unresolvedLabels: unresolvedLabels.sorted()
        )

        let notReadyLabels = readiness.unavailableLabels + readiness.unresolvedLabels
        if notReadyLabels.isEmpty == false {
            print("Porthole loaded configuration '\(configuration.name)' before all reference state was ready: \(notReadyLabels)")
        }
        return readiness
    }

    private static func requireLoadedReferenceState(
        _ configuration: CellConfiguration,
        controlCell: OrchestratorCell,
        requester: Identity
    ) async throws {
        let readiness = await waitForLoadedReferenceState(
            configuration,
            controlCell: controlCell,
            requester: requester
        )
        guard readiness.unavailableLabels.isEmpty,
              readiness.unresolvedLabels.isEmpty else {
            throw Abort(
                .unprocessableEntity,
                reason: "Configuration '\(configuration.name)' is not runtime-ready: "
                    + "unavailable=\(readiness.unavailableLabels), "
                    + "unresolved=\(readiness.unresolvedLabels)."
            )
        }
    }

    static func requireLoadedReferenceStateRestoringPrevious(
        _ configuration: CellConfiguration,
        previousConfiguration: CellConfiguration?,
        previousReferenceRequestersByLabel: [String: Identity],
        controlCell: OrchestratorCell,
        requester: Identity,
        loadRequester: Identity
    ) async throws {
        do {
            try await requireLoadedReferenceState(
                configuration,
                controlCell: controlCell,
                requester: requester
            )
        } catch {
            try await restorePreviousPortholeConfiguration(
                rejectedConfigurationName: configuration.name,
                failureSummary: "failed readiness",
                previousConfiguration: previousConfiguration,
                previousReferenceRequestersByLabel: previousReferenceRequestersByLabel,
                controlCell: controlCell,
                loadRequester: loadRequester
            )
            throw error
        }
    }

    private static func restorePreviousPortholeConfiguration(
        rejectedConfigurationName: String,
        failureSummary: String,
        previousConfiguration: CellConfiguration?,
        previousReferenceRequestersByLabel: [String: Identity],
        controlCell: OrchestratorCell,
        loadRequester: Identity
    ) async throws {
        let restorationConfiguration = previousConfiguration
            ?? CellConfiguration(name: "Empty Porthole")
        do {
            try await loadPortholeConfiguration(
                restorationConfiguration,
                controlCell: controlCell,
                requester: loadRequester,
                referenceRequestersByLabel: previousReferenceRequestersByLabel
            )
        } catch let restorationError {
            print(
                "Porthole failed restoring the previous configuration after '\(rejectedConfigurationName)' "
                    + "\(failureSummary): \(restorationError)"
            )
            throw Abort(
                .internalServerError,
                reason: "The requested Porthole configuration failed and the previous configuration could not be restored."
            )
        }
    }

    static func readLoadedReferenceState(
        _ target: Meddle,
        label: String,
        requester: Identity
    ) async -> BootstrapReadResult {
        if let runtimeReady = target as? CellRuntimeReady {
            do {
                try await runtimeReady.ensureRuntimeReady()
            } catch {
                return .unavailable
            }
        }
        if let generalCell = target as? GeneralCell {
            let decision = await generalCell.authorizationDecision(
                requestedAccess: "r---",
                at: "state",
                for: requester
            )
            guard decision.allowed else {
                return .accessDenied(
                    decision.userMessage
                        ?? decision.reasonCode
                        ?? decision.reason
                )
            }
        }
        do {
            let value = try await getReferencedTarget(
                target,
                nestedKeypath: "state",
                fullKeypath: "\(label).state",
                requester: requester
            )
            if let denialReason = accessDenialReason(from: value)
                ?? proofLookupFailureReason(from: value) {
                return .accessDenied(denialReason)
            }
            return .value(value)
        } catch {
            let message = String(describing: error)
            if let denialReason = proofLookupFailureReason(from: .string(message))
                ?? accessDenialReason(from: message) {
                return .accessDenied(denialReason)
            }
            return .unavailable
        }
    }

    private static func disableFeedSubscriptions(_ reference: CellReference) -> CellReference {
        var sanitized = reference
        sanitized.subscribeFeed = shouldPreserveWebFeedSubscription(reference)
        sanitized.subscriptions = reference.subscriptions.map(disableFeedSubscriptions)
        return sanitized
    }

    private static func shouldPreserveWebFeedSubscription(_ reference: CellReference) -> Bool {
        let normalizedEndpoint = reference.endpoint
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        let normalizedLabel = reference.label
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
        return normalizedEndpoint == "cell:///aiassistantthread"
            || normalizedLabel == "aiassistantthread"
            || normalizedEndpoint == "cell:///conferencesessionthreadlive"
            || normalizedEndpoint == "cell:///conferencesessionthreadshared"
            || normalizedLabel == "conferencesessionthread"
    }

    private static func sharedWorkbenchReferenceRequesters(
        configuration: CellConfiguration,
        requester: Identity
    ) async throws -> [String: Identity]? {
        let normalizedName = configuration.name.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        let normalizedUUID = configuration.uuid.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        guard normalizedName == WorkbenchAccessGrantCell.sharedWorkbenchConfigurationName.lowercased()
                || normalizedUUID.hasPrefix("shared-workbench-") else {
            return nil
        }

        var requestersByLabel = [String: Identity]()
        for reference in configuration.cellReferences ?? [] {
            guard let concreteEndpoint = WorkbenchAccessGrantCell.sharedWorkbenchConcreteEndpoint(
                in: configuration,
                label: reference.label,
                sourceEndpoint: reference.endpoint
            ) else {
                continue
            }
            guard concreteEndpoint.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
                    == reference.endpoint.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() else {
                throw Abort(
                    .unprocessableEntity,
                    reason: "Shared Workbench target '\(reference.label)' is not pinned to its invitation endpoint."
                )
            }
            guard let targetOwner = await WorkbenchAccessGrantCell.sharedWorkbenchTargetLookupRequester(
                configuration: configuration,
                label: reference.label,
                endpoint: concreteEndpoint,
                requester: requester
            ) else {
                throw Abort(
                    .unprocessableEntity,
                    reason: "Shared Workbench target '\(reference.label)' has no proof-capable owner authority."
                )
            }
            requestersByLabel[reference.label] = targetOwner
        }
        guard requestersByLabel.isEmpty == false else {
            throw Abort(.unprocessableEntity, reason: "Shared Workbench has no invitation-bound target references.")
        }
        return requestersByLabel
    }

    private static func referenceRequestersForLoading(
        configuration: CellConfiguration,
        requester: Identity,
        fallbackRequester: Identity
    ) async throws -> [String: Identity] {
        let sharedRequesters = try await sharedWorkbenchReferenceRequesters(
            configuration: configuration,
            requester: requester
        ) ?? [:]
        var requestersByLabel = [String: Identity]()
        for reference in configuration.cellReferences ?? [] {
            if let sharedRequester = sharedRequesters[reference.label] {
                requestersByLabel[reference.label] = sharedRequester
                continue
            }
            let resolvedReference = resolvedSharedWorkbenchReference(
                for: reference,
                label: reference.label,
                configuration: configuration
            )
            requestersByLabel[reference.label] = await referenceResolutionRequester(
                for: resolvedReference,
                label: reference.label,
                configuration: configuration,
                requester: requester,
                referenceLookupRequester: fallbackRequester
            )
        }
        return requestersByLabel
    }

    static func loadRequestedConfiguration(
        from payload: ValueType,
        controlCell: OrchestratorCell,
        requester: Identity
    ) async throws -> CellConfiguration {
        guard let configuration = try await resolveRequestedCellConfiguration(
            from: payload,
            controlCell: controlCell,
            requester: requester
        ) else {
            throw Abort(.badRequest, reason: "Configuration is not available in this Porthole yet.")
        }
        guard ConfigurationCatalogCell.isPortholePublishedConfiguration(configuration) else {
            throw Abort(
                .unprocessableEntity,
                reason: "Configuration '\(configuration.name)' is not web-ready in this Porthole yet."
            )
        }

        _ = await ConferencePreviewWrapperResolverSupport.resetStalePreviewMappingsIfNeeded(
            for: configuration,
            requester: requester
        )

        let loadRequester = await ownerRequester(for: controlCell, requester: requester)
        let sourceBackedConfiguration = await EditableCellConfigurationOverlayResolver.overlay(
            configuration: configuration,
            requester: requester
        )
        let loadConfiguration = portholeWebLoadConfiguration(sourceBackedConfiguration)
        let previousConfiguration = controlCell.getCellConfiguration()
        let previousReferenceRequesters = if let previousConfiguration {
            (try? await referenceRequestersForLoading(
                configuration: previousConfiguration,
                requester: requester,
                fallbackRequester: loadRequester
            )) ?? [:]
        } else {
            [String: Identity]()
        }
        let referenceRequesters = try await referenceRequestersForLoading(
            configuration: loadConfiguration,
            requester: requester,
            fallbackRequester: loadRequester
        )

        func loadConfigurationOnce() async throws {
            try await loadPortholeConfiguration(
                loadConfiguration,
                controlCell: controlCell,
                requester: loadRequester,
                referenceRequestersByLabel: referenceRequesters
            )
        }

        func loadConfigurationRecoveringUnavailableWorkbenchAccessGrant() async throws {
            do {
                try await loadConfigurationOnce()
            } catch {
                guard isWorkbenchAccessGrantConfiguration(loadConfiguration),
                      isPersistedCellUnavailable(error),
                      await resetStaleWorkbenchAccessGrantSharedMappingIfNeeded(
                        requester: requester
                      ) else {
                    throw error
                }
                try await loadConfigurationOnce()
            }
        }

        if isSameActiveConfiguration(controlCell.getCellConfiguration(), as: configuration) {
            do {
                try await loadConfigurationRecoveringUnavailableWorkbenchAccessGrant()
            } catch {
                print("Porthole failed refreshing active configuration '\(configuration.name)' from \(configuration.discovery?.sourceCellEndpoint ?? "unknown endpoint"): \(error)")
                try await restorePreviousPortholeConfiguration(
                    rejectedConfigurationName: configuration.name,
                    failureSummary: "could not be refreshed",
                    previousConfiguration: previousConfiguration,
                    previousReferenceRequestersByLabel: previousReferenceRequesters,
                    controlCell: controlCell,
                    loadRequester: loadRequester
                )
                if let abort = adminRemoteBridgeAbort(
                    for: error,
                    configurationName: configuration.name,
                    operation: "refreshed"
                ) {
                    throw abort
                }
                throw Abort(
                    .unprocessableEntity,
                    reason: "Configuration '\(configuration.name)' could not be refreshed in this Porthole."
                )
            }
            try await requireLoadedReferenceStateRestoringPrevious(
                loadConfiguration,
                previousConfiguration: previousConfiguration,
                previousReferenceRequestersByLabel: previousReferenceRequesters,
                controlCell: controlCell,
                requester: requester,
                loadRequester: loadRequester
            )
            await resetLoadedConfigurationLandingStateIfNeeded(
                loadConfiguration,
                controlCell: controlCell,
                requester: loadRequester
            )
            return loadConfiguration
        }

        do {
            try await loadConfigurationRecoveringUnavailableWorkbenchAccessGrant()
        } catch {
            print("Porthole failed loading configuration '\(configuration.name)' from \(configuration.discovery?.sourceCellEndpoint ?? "unknown endpoint") on first attempt: \(error)")
            if let abort = adminRemoteBridgeAbort(
                for: error,
                configurationName: configuration.name,
                operation: "loaded"
            ) {
                try await restorePreviousPortholeConfiguration(
                    rejectedConfigurationName: configuration.name,
                    failureSummary: "could not be loaded",
                    previousConfiguration: previousConfiguration,
                    previousReferenceRequestersByLabel: previousReferenceRequesters,
                    controlCell: controlCell,
                    loadRequester: loadRequester
                )
                throw abort
            }
            try? await Task.sleep(nanoseconds: 250_000_000)
            do {
                try await loadConfigurationRecoveringUnavailableWorkbenchAccessGrant()
                print("Porthole loaded configuration '\(configuration.name)' after retry.")
            } catch {
                print("Porthole failed loading configuration '\(configuration.name)' from \(configuration.discovery?.sourceCellEndpoint ?? "unknown endpoint") after retry: \(error)")
                try await restorePreviousPortholeConfiguration(
                    rejectedConfigurationName: configuration.name,
                    failureSummary: "could not be loaded",
                    previousConfiguration: previousConfiguration,
                    previousReferenceRequestersByLabel: previousReferenceRequesters,
                    controlCell: controlCell,
                    loadRequester: loadRequester
                )
                if let abort = adminRemoteBridgeAbort(
                    for: error,
                    configurationName: configuration.name,
                    operation: "loaded"
                ) {
                    throw abort
                }
                throw Abort(
                    .unprocessableEntity,
                    reason: "Configuration '\(configuration.name)' could not be loaded in this Porthole."
                )
            }
        }
        try await requireLoadedReferenceStateRestoringPrevious(
            loadConfiguration,
            previousConfiguration: previousConfiguration,
            previousReferenceRequestersByLabel: previousReferenceRequesters,
            controlCell: controlCell,
            requester: requester,
            loadRequester: loadRequester
        )
        await resetLoadedConfigurationLandingStateIfNeeded(
            loadConfiguration,
            controlCell: controlCell,
            requester: loadRequester
        )

        return loadConfiguration
    }

    static func adminRemoteBridgeAbort(
        for error: Error,
        configurationName: String,
        operation: String
    ) -> Abort? {
        guard let transportError = error as? AdminAuthenticatedVaporBridgeTransportError else {
            return nil
        }
        return Abort(
            .serviceUnavailable,
            reason: "Configuration '\(configurationName)' could not be \(operation) because its remote AdminScaffold is unavailable. \(transportError.localizedDescription)"
        )
    }

    private static func isSameActiveConfiguration(_ active: CellConfiguration?, as requested: CellConfiguration) -> Bool {
        guard let active else { return false }
        let activeName = normalizedConfigurationIdentity(active.name)
        let requestedName = normalizedConfigurationIdentity(requested.name)
        guard activeName.isEmpty == false, activeName == requestedName else { return false }

        let activeEndpoint = normalizedConfigurationIdentity(active.discovery?.sourceCellEndpoint)
        let requestedEndpoint = normalizedConfigurationIdentity(requested.discovery?.sourceCellEndpoint)
        if activeEndpoint.isEmpty == false || requestedEndpoint.isEmpty == false {
            if activeEndpoint == requestedEndpoint,
               isLegacyCoPilotChatResourceRouter(active),
               isPersonalChatHubConfiguration(requested) {
                return false
            }
            return activeEndpoint == requestedEndpoint
        }

        let activeUUID = active.uuid.trimmingCharacters(in: .whitespacesAndNewlines)
        let requestedUUID = requested.uuid.trimmingCharacters(in: .whitespacesAndNewlines)
        if activeUUID.isEmpty == false,
           requestedUUID.isEmpty == false {
            return activeUUID == requestedUUID
        }

        return true
    }

    private static func normalizedConfigurationIdentity(_ value: String?) -> String {
        (value ?? "")
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()
    }

    static func resetLoadedConfigurationLandingStateIfNeeded(
        _ configuration: CellConfiguration,
        controlCell: OrchestratorCell,
        requester: Identity
    ) async {
        guard configuration.name == "Conference Participant Portal Dashboard" else {
            return
        }

        let participantReferenceLabels = (configuration.cellReferences ?? [])
            .filter { reference in
                let endpoint = reference.endpoint.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
                return endpoint == "cell:///conferenceparticipantpreviewshell"
                    || endpoint == "cell:///conferenceparticipantshell"
            }
            .map(\.label)

        let candidateLabels = participantReferenceLabels.isEmpty
            ? ["conferenceParticipantShell"]
            : participantReferenceLabels

        let resetPayload: ValueType = .object([
            "trigger": .string("configuration-load-default"),
            "selectedValue": .string("today"),
            "id": .string("today")
        ])

        for label in candidateLabels {
            guard let target = await referencedActionTarget(
                controlCell: controlCell,
                label: label,
                requester: requester
            ) else {
                continue
            }
            _ = try? await target.set(
                keypath: "navigation.setActiveTab",
                value: resetPayload,
                requester: requester
            )
            return
        }
    }

    private static func executeEditorActionIfNeeded(
        controlCell: OrchestratorCell,
        sessionId: String,
        keypath: String,
        payload: ValueType?,
        requester: Identity
    ) async throws -> ValueType? {
        guard keypath.hasPrefix("editor.") else { return nil }

        let currentCommitted = controlCell.getCellConfiguration()
        let editableConfigurationState = await currentEditableState(
            for: currentCommitted,
            requester: requester
        )
        let committedBaseConfiguration = editorCommittedConfiguration(
            currentConfiguration: currentCommitted,
            editableConfigurationState: editableConfigurationState
        )
        let committedConfiguration = configurationWithDefaultChatWorkbench(
            committedBaseConfiguration
        )
        var editorState = PortholeEditorSessionStore.shared.sync(
            sessionId: sessionId,
            committedConfiguration: committedConfiguration,
            committedSourceRevision: editableConfigurationState?.revision
        )

        switch keypath {
        case "editor.mode.set":
            guard let mode = extractEditorMode(from: payload) else {
                throw Abort(.badRequest, reason: "editor.mode.set requires mode=view|edit")
            }
            if editableConfigurationState != nil, mode == .edit {
                try assertEditableInPorthole(editableConfigurationState)
            }

            var responseEditableConfigurationState = editableConfigurationState
            var mutationCommittedConfiguration = committedConfiguration
            if mode == .view, editorState.isDirty {
                try await applyWorkingDocument(
                    editorState.currentWorkingDocument,
                    expectedSourceRevision: editorState.committedSourceRevision,
                    to: controlCell,
                    requester: requester
                )
                responseEditableConfigurationState = await currentEditableState(
                    for: controlCell.getCellConfiguration(),
                    requester: requester
                )
                let mutationBaseConfiguration = editorCommittedConfiguration(
                    currentConfiguration: controlCell.getCellConfiguration(),
                    editableConfigurationState: responseEditableConfigurationState
                )
                mutationCommittedConfiguration = configurationWithDefaultChatWorkbench(
                    mutationBaseConfiguration
                )
            }

            editorState = PortholeEditorSessionStore.shared.mutate(
                sessionId: sessionId,
                committedConfiguration: mutationCommittedConfiguration,
                committedSourceRevision: responseEditableConfigurationState?.revision
            ) { state in
                state.mode = mode
                if mode == .edit {
                    if state.workingDocument == nil {
                        state.workingDocument = state.committedDocument
                    }
                    if state.selectionPath == nil, state.workingDocument?.skeleton != nil {
                        state.selectionPath = "root"
                    }
                } else {
                    state.selectionPath = nil
                    state.undoStack.removeAll()
                    state.redoStack.removeAll()
                    state.workingDocument = state.committedDocument
                }
                state.revision &+= 1
            }
            return makeActionEnvelope(
                actionKeypath: keypath,
                result: .string("ok"),
                editorState: editorState,
                includeDocumentSnapshots: true,
                editableConfigurationState: responseEditableConfigurationState
            )

        case "editor.selection.set":
            editorState = PortholeEditorSessionStore.shared.mutate(
                sessionId: sessionId,
                committedConfiguration: committedConfiguration,
                committedSourceRevision: editableConfigurationState?.revision
            ) { state in
                state.selectionPath = extractSelectionPath(from: payload)
                state.revision &+= 1
            }
            return makeActionEnvelope(
                actionKeypath: keypath,
                result: .string("ok"),
                editorState: editorState,
                includeDocumentSnapshots: true,
                editableConfigurationState: editableConfigurationState
            )

        case "editor.working.setSkeleton":
            if editableConfigurationState != nil {
                try assertEditableInPorthole(editableConfigurationState)
            }
            guard let payload else {
                throw Abort(.badRequest, reason: "editor.working.setSkeleton requires payload")
            }
            guard let skeleton = decodeSkeletonElement(from: payload) else {
                throw Abort(.badRequest, reason: "Unable to decode working skeleton payload")
            }

            editorState = PortholeEditorSessionStore.shared.mutate(
                sessionId: sessionId,
                committedConfiguration: committedConfiguration,
                committedSourceRevision: editableConfigurationState?.revision
            ) { state in
                if state.mode != .edit {
                    state.mode = .edit
                }
                if state.workingDocument == nil {
                    state.workingDocument = state.committedDocument
                }
                let current = state.currentWorkingDocument
                if current.skeleton != nil || current.references.isEmpty == false {
                    state.undoStack.append(current)
                }
                var updated = current
                updated.skeleton = skeleton
                state.workingDocument = updated
                state.redoStack.removeAll()
                if state.selectionPath == nil {
                    state.selectionPath = "root"
                }
                state.revision &+= 1
            }
            return makeActionEnvelope(
                actionKeypath: keypath,
                result: .string("ok"),
                editorState: editorState,
                includeDocumentSnapshots: true,
                editableConfigurationState: editableConfigurationState
            )

        case "editor.component.insert":
            if editableConfigurationState != nil {
                try assertEditableInPorthole(editableConfigurationState)
            }
            guard let payload,
                  let insertionPayload = decodeComponentInsertionPayload(from: payload) else {
                throw Abort(.badRequest, reason: "editor.component.insert krever component + placement.")
            }

            var insertionResult: PortholeWebComponentInsertionResult?
            var insertionError: Error?
            editorState = PortholeEditorSessionStore.shared.mutate(
                sessionId: sessionId,
                committedConfiguration: committedConfiguration,
                committedSourceRevision: editableConfigurationState?.revision
            ) { state in
                if state.mode != .edit {
                    state.mode = .edit
                }
                if state.workingDocument == nil {
                    state.workingDocument = state.committedDocument
                }

                let current = state.currentWorkingDocument
                do {
                    let inserted = try PortholeWebComponentInsertionService.insert(
                        component: insertionPayload.component,
                        into: current,
                        placement: insertionPayload.placement
                    )
                    state.undoStack.append(current)
                    state.workingDocument = inserted.updatedDocument
                    state.redoStack.removeAll()
                    state.selectionPath = inserted.targetPath
                    state.revision &+= 1
                    insertionResult = inserted
                } catch {
                    insertionError = error
                }
            }

            if let insertionError {
                throw Abort(.unprocessableEntity, reason: insertionError.localizedDescription)
            }
            guard let insertionResult else {
                throw Abort(.unprocessableEntity, reason: "Komponenten kunne ikke plasseres.")
            }

            return makeActionEnvelope(
                actionKeypath: keypath,
                result: .object([
                    "status": .string("inserted"),
                    "componentName": .string(insertionResult.insertedComponentName),
                    "targetPath": .string(insertionResult.targetPath),
                    "referenceLabels": .list(insertionResult.insertedReferenceLabels.map { .string($0) })
                ]),
                editorState: editorState,
                includeDocumentSnapshots: true,
                editableConfigurationState: editableConfigurationState
            )

        case "editor.undo":
            if editableConfigurationState != nil {
                try assertEditableInPorthole(editableConfigurationState)
            }
            editorState = PortholeEditorSessionStore.shared.mutate(
                sessionId: sessionId,
                committedConfiguration: committedConfiguration,
                committedSourceRevision: editableConfigurationState?.revision
            ) { state in
                guard let previous = state.undoStack.popLast() else { return }
                let current = state.currentWorkingDocument
                if current.skeleton != nil || current.references.isEmpty == false {
                    state.redoStack.append(current)
                }
                state.workingDocument = previous
                state.revision &+= 1
            }
            return makeActionEnvelope(
                actionKeypath: keypath,
                result: .string("ok"),
                editorState: editorState,
                includeDocumentSnapshots: true,
                editableConfigurationState: editableConfigurationState
            )

        case "editor.redo":
            if editableConfigurationState != nil {
                try assertEditableInPorthole(editableConfigurationState)
            }
            editorState = PortholeEditorSessionStore.shared.mutate(
                sessionId: sessionId,
                committedConfiguration: committedConfiguration,
                committedSourceRevision: editableConfigurationState?.revision
            ) { state in
                guard let next = state.redoStack.popLast() else { return }
                let current = state.currentWorkingDocument
                if current.skeleton != nil || current.references.isEmpty == false {
                    state.undoStack.append(current)
                }
                state.workingDocument = next
                state.revision &+= 1
            }
            return makeActionEnvelope(
                actionKeypath: keypath,
                result: .string("ok"),
                editorState: editorState,
                includeDocumentSnapshots: true,
                editableConfigurationState: editableConfigurationState
            )

        case "editor.discard":
            if editableConfigurationState != nil {
                try assertEditableInPorthole(editableConfigurationState)
            }
            editorState = PortholeEditorSessionStore.shared.mutate(
                sessionId: sessionId,
                committedConfiguration: committedConfiguration,
                committedSourceRevision: editableConfigurationState?.revision
            ) { state in
                state.workingDocument = state.committedDocument
                state.undoStack.removeAll()
                state.redoStack.removeAll()
                state.selectionPath = state.mode == .edit && state.workingDocument?.skeleton != nil ? "root" : nil
                state.revision &+= 1
            }
            return makeActionEnvelope(
                actionKeypath: keypath,
                result: .string("ok"),
                editorState: editorState,
                includeDocumentSnapshots: true,
                editableConfigurationState: editableConfigurationState
            )

        case "editor.apply":
            if editableConfigurationState != nil {
                try assertEditableInPorthole(editableConfigurationState)
            }
            guard editorState.isDirty else {
                return makeActionEnvelope(
                    actionKeypath: keypath,
                    result: .string("noop"),
                    editorState: editorState,
                    includeDocumentSnapshots: true,
                    editableConfigurationState: editableConfigurationState
                )
            }

            try await applyWorkingDocument(
                editorState.currentWorkingDocument,
                expectedSourceRevision: editorState.committedSourceRevision,
                to: controlCell,
                requester: requester
            )
            let refreshedEditableState = await currentEditableState(
                for: controlCell.getCellConfiguration(),
                requester: requester
            )
            let refreshedBaseConfiguration = editorCommittedConfiguration(
                currentConfiguration: controlCell.getCellConfiguration(),
                editableConfigurationState: refreshedEditableState
            )
            let refreshedCommittedConfiguration = configurationWithDefaultChatWorkbench(
                refreshedBaseConfiguration
            )
            editorState = PortholeEditorSessionStore.shared.mutate(
                sessionId: sessionId,
                committedConfiguration: refreshedCommittedConfiguration,
                committedSourceRevision: refreshedEditableState?.revision
            ) { state in
                state.workingDocument = state.committedDocument
                state.undoStack.removeAll()
                state.redoStack.removeAll()
                if state.mode == .edit {
                    state.selectionPath = "root"
                }
                state.revision &+= 1
            }
            return makeActionEnvelope(
                actionKeypath: keypath,
                result: .string("applied"),
                editorState: editorState,
                includeDocumentSnapshots: true,
                editableConfigurationState: refreshedEditableState
            )

        default:
            throw Abort(.badRequest, reason: "Unsupported editor action keypath: \(keypath)")
        }
    }

    private static func applyWorkingDocument(
        _ workingDocument: PortholeEditorDocumentSnapshot,
        expectedSourceRevision: Int?,
        to controlCell: OrchestratorCell,
        requester: Identity
    ) async throws {
        let currentConfiguration = controlCell.getCellConfiguration()
        if let editableConfigurationState = await currentEditableState(
            for: currentConfiguration,
            requester: requester
        ) {
            try assertEditableInPorthole(editableConfigurationState)
            var configuration = editableConfigurationState.configuration
            configuration.skeleton = workingDocument.skeleton
            configuration.cellReferences = workingDocument.references.isEmpty ? nil : workingDocument.references
            let appliedState = try await EditableCellConfigurationOverlayResolver.apply(
                configuration,
                expectedRevision: expectedSourceRevision,
                to: currentConfiguration ?? configuration,
                requester: requester
            )
            try await controlCell.setCellConfiguration(cellConfig: appliedState.configuration)
            return
        }
        var configuration = currentConfiguration ?? CellConfiguration(name: "Porthole")
        configuration.skeleton = workingDocument.skeleton
        configuration.cellReferences = workingDocument.references.isEmpty ? nil : workingDocument.references
        try await controlCell.setCellConfiguration(cellConfig: configuration)
    }

    private static func currentEditableState(
        for configuration: CellConfiguration?,
        requester: Identity
    ) async -> EditableCellConfigurationContract.State? {
        guard let configuration else { return nil }
        return await EditableCellConfigurationOverlayResolver.matchingEditableState(
            for: configuration,
            requester: requester
        )
    }

    private static func editorCommittedConfiguration(
        currentConfiguration: CellConfiguration?,
        editableConfigurationState: EditableCellConfigurationContract.State?
    ) -> CellConfiguration? {
        guard let editableConfigurationState else {
            return currentConfiguration
        }
        guard editableConfigurationState.hasStoredOverride == false,
              let currentConfiguration else {
            return editableConfigurationState.configuration
        }

        let currentSkeletonSignature = editorSkeletonSignature(currentConfiguration.skeleton)
        let sourceFallbackSkeletonSignature = editorSkeletonSignature(
            editableConfigurationState.fallbackConfiguration.skeleton
        )
        if currentSkeletonSignature.isEmpty == false,
           sourceFallbackSkeletonSignature.isEmpty == false,
           currentSkeletonSignature != sourceFallbackSkeletonSignature {
            return currentConfiguration
        }
        return editableConfigurationState.configuration
    }

    private static func editorSkeletonSignature(_ skeleton: SkeletonElement?) -> String {
        guard let skeleton else { return "" }
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.sortedKeys]
        guard let data = try? encoder.encode(skeleton),
              let encoded = String(data: data, encoding: .utf8) else {
            return ""
        }
        return encoded
    }

    private static func assertEditableInPorthole(
        _ editableConfigurationState: EditableCellConfigurationContract.State?
    ) throws {
        guard let editableConfigurationState, editableConfigurationState.canEdit == false else {
            return
        }

        let summary = editableConfigurationState.accessSummary.trimmingCharacters(in: .whitespacesAndNewlines)
        let reason = summary.isEmpty
            ? editorReadOnlyMessage(for: editableConfigurationState)
            : "\(editorReadOnlyMessage(for: editableConfigurationState)) \(summary)"
        throw Abort(.unprocessableEntity, reason: reason)
    }

    private static func makeActionEnvelope(
        actionKeypath: String,
        result: ValueType,
        editorState: PortholeEditorSessionState,
        includeDocumentSnapshots: Bool,
        editableConfigurationState: EditableCellConfigurationContract.State? = nil
    ) -> ValueType {
        .object([
            "contractVersion": .string("porthole-web-v2"),
            "ok": .bool(true),
            "action": .string(actionKeypath),
            "result": result,
            "editorState": makeEditorStateValue(
                editorState,
                includeDocumentSnapshots: includeDocumentSnapshots,
                editableConfigurationState: editableConfigurationState
            )
        ])
    }

    private static func makeEditorStateValue(
        _ editorState: PortholeEditorSessionState,
        includeDocumentSnapshots: Bool,
        editableConfigurationState: EditableCellConfigurationContract.State? = nil
    ) -> ValueType {
        var object: Object = [
            "mode": .string(editorState.mode.rawValue),
            "isEditing": .bool(editorState.mode == .edit),
            "isDirty": .bool(editorState.isDirty),
            "selectionPath": editorState.selectionPath.map { .string($0) } ?? .null,
            "canUndo": .bool(!editorState.undoStack.isEmpty),
            "canRedo": .bool(!editorState.redoStack.isEmpty),
            "undoDepth": .integer(editorState.undoStack.count),
            "redoDepth": .integer(editorState.redoStack.count),
            "revision": .integer(editorState.revision),
            "committedSourceRevision": editorState.committedSourceRevision.map(ValueType.integer) ?? .null,
            "workingSkeleton": includeDocumentSnapshots ? encodeSkeletonValue(editorState.workingSkeleton) : .null,
            "committedSkeleton": includeDocumentSnapshots ? encodeSkeletonValue(editorState.committedSkeleton) : .null,
            "workingReferences": includeDocumentSnapshots ? encodeReferencesValue(editorState.workingReferences) : .list([]),
            "committedReferences": includeDocumentSnapshots ? encodeReferencesValue(editorState.committedReferences) : .list([]),
            "workingCopy": includeDocumentSnapshots ? encodeSkeletonValue(editorState.workingSkeleton) : .null,
            "viewerSnapshot": includeDocumentSnapshots ? encodeSkeletonValue(editorState.committedSkeleton) : .null,
            "sourceBacked": .bool(editableConfigurationState != nil),
            "canEdit": .bool(editableConfigurationState?.canEdit ?? true),
            "sourceCellEndpoint": editableConfigurationState.map { .string($0.sourceCellEndpoint) } ?? .null,
            "sourceCellName": editableConfigurationState.map { .string($0.sourceCellName) } ?? .null,
            "accessSummary": editableConfigurationState.map { .string($0.accessSummary) } ?? .null
        ]
        if let editableConfigurationState {
            object["accessInstruction"] = .string(editorAccessInstruction(for: editableConfigurationState))
        } else {
            object["accessInstruction"] = .string("Denne CellConfigurationen redigeres lokalt i Porthole til du trykker Apply.")
        }
        return .object(object)
    }

    private static func editorReadOnlyMessage(
        for state: EditableCellConfigurationContract.State
    ) -> String {
        "Denne CellConfigurationen kan leses, men ikke redigeres av nåværende requester i Porthole. Åpne Porthole som eier av \(state.sourceCellEndpoint), eller be eier gi en Agreement-grant med rw-- for \(EditableCellConfigurationContract.applyKeypath)."
    }

    private static func editorAccessInstruction(
        for state: EditableCellConfigurationContract.State
    ) -> String {
        if state.canEdit {
            return "Endringer kan lagres til \(state.sourceCellEndpoint) via \(EditableCellConfigurationContract.applyKeypath)."
        }
        return editorReadOnlyMessage(for: state)
    }

    private static func makeLegacyEditorValue(_ editorState: PortholeEditorSessionState) -> ValueType {
        .object([
            "mode": .string(editorState.mode.rawValue),
            "panels": .list([.string("elements"), .string("inspector")]),
            "selectionPath": editorState.selectionPath.map { .string($0) } ?? .null,
            "isDirty": .bool(editorState.isDirty),
            "canUndo": .bool(!editorState.undoStack.isEmpty),
            "canRedo": .bool(!editorState.redoStack.isEmpty),
            "notes": .string("Porthole web editor contract v2")
        ])
    }

    private static func extractEditorMode(from payload: ValueType?) -> PortholeEditorMode? {
        guard let payload else { return nil }
        let rawMode: String?
        if case let .string(value) = payload {
            rawMode = value
        } else if case let .object(object) = payload,
                  case let .string(value)? = object["mode"] {
            rawMode = value
        } else {
            rawMode = nil
        }

        guard let rawMode else { return nil }
        return PortholeEditorMode(rawValue: rawMode.trimmingCharacters(in: .whitespacesAndNewlines).lowercased())
    }

    private static func extractSelectionPath(from payload: ValueType?) -> String? {
        guard let payload else { return nil }
        if case .null = payload {
            return nil
        }
        if case let .string(path) = payload {
            let trimmed = path.trimmingCharacters(in: .whitespacesAndNewlines)
            return trimmed.isEmpty ? nil : trimmed
        }
        if case let .object(object) = payload {
            if case .null? = object["path"] {
                return nil
            }
            if case let .string(path)? = object["path"] {
                let trimmed = path.trimmingCharacters(in: .whitespacesAndNewlines)
                return trimmed.isEmpty ? nil : trimmed
            }
        }
        return nil
    }

    private static func decodeSkeletonElement(from value: ValueType) -> SkeletonElement? {
        SkeletonRuntimeDecoder.decode(from: value)
    }

    private static func encodeSkeletonValue(_ skeleton: SkeletonElement?) -> ValueType {
        guard let skeleton else { return .null }
        let encoder = JSONEncoder()
        guard let data = try? encoder.encode(skeleton),
              let value = try? JSONDecoder().decode(ValueType.self, from: data) else {
            return .null
        }
        return value
    }

    private static func encodeReferencesValue(_ references: [CellReference]) -> ValueType {
        encodeCodableValue(references)
    }

    private static func encodeCodableValue<T: Encodable>(_ value: T) -> ValueType {
        let encoder = JSONEncoder()
        guard let data = try? encoder.encode(value),
              let wrapped = try? JSONDecoder().decode(ValueType.self, from: data) else {
            return .null
        }
        return wrapped
    }

    private static func decodeComponentInsertionPayload(from value: ValueType) -> PortholeWebComponentInsertionPayload? {
        guard let json = try? value.jsonString() else { return nil }
        return try? JSONDecoder().decode(PortholeWebComponentInsertionPayload.self, fromString: json)
    }

    private static func extractLabel(from value: ValueType?) -> String? {
        guard let value else { return nil }
        if case let .string(label) = value {
            return label
        }
        if case let .object(object) = value,
           case let .string(label)? = object["label"] {
            return label
        }
        return nil
    }

    private static func requestContainsConferencePersonaQuery(in req: Request) -> Bool {
        guard let query = req.url.query, query.isEmpty == false,
              let components = URLComponents(string: "https://porthole.invalid/?\(query)") else {
            return false
        }
        return components.queryItems?.contains(where: { $0.name == conferencePersonaQueryKey }) ?? false
    }

    private static func conferencePersonasEnabled(in req: Request) -> Bool {
        if req.application.environment == .testing {
            return true
        }
        guard req.application.environment == .development else {
            return false
        }
        return RuntimeEnvironmentParsing.bool(
            Environment.get(conferencePersonaDevelopmentOptInEnvironmentKey)
        ) == true
    }

    private static func requesterSnapshot(
        _ requester: Identity,
        conferencePersonaId: String?,
        conferencePersonaWarning: String? = nil
    ) -> ValueType {
        var object: Object = [
            "uuid": .string(requester.uuid),
            "signingKeyFingerprint": requester.signingPublicKeyFingerprint.map(ValueType.string) ?? .null,
            "displayName": requester.displayName.isEmpty ? .null : .string(requester.displayName),
            "conferencePersonaId": conferencePersonaId.map(ValueType.string) ?? .null,
            "conferencePersonaWarning": conferencePersonaWarning.map(ValueType.string) ?? .null
        ]

        if let conferencePersonaId,
           let persona = try? ConferencePlaywrightPersonaBootstrap.persona(id: conferencePersonaId) {
            object["conferencePersonaDisplayName"] = .string(persona.displayName)
            object["conferencePersonaRole"] = .string(persona.role)
        } else {
            object["conferencePersonaDisplayName"] = .null
            object["conferencePersonaRole"] = .null
        }

        return .object(object)
    }

    private static func bridgePresenceValue(for requester: Identity) -> ValueType {
        let participantID = requester.uuid.trimmingCharacters(in: .whitespacesAndNewlines)
        let topics = [
            ScaffoldNotificationContracts.workflowRunTopic,
            ScaffoldNotificationContracts.workflowReviewTopic,
            ScaffoldNotificationContracts.workflowRemoteTopic
        ]

        return .object([
            "enabled": .bool(participantID.isEmpty == false),
            "participantId": participantID.isEmpty ? .null : .string(participantID),
            "deviceIdStorageKey": .string("porthole.bridge.deviceId.\(participantID.isEmpty ? "default" : participantID)"),
            "deviceIdPrefix": .string("porthole-web"),
            "topics": .list(topics.map(ValueType.string))
        ])
    }

    static func notificationSummary(fromOutboxState outboxState: ValueType?) -> ValueType {
        let defaultValue: ValueType = .object([
            "connected": .bool(false),
            "totalTickets": .integer(0),
            "queuedTickets": .integer(0),
            "openTickets": .integer(0),
            "ackedTickets": .integer(0),
            "items": .list([]),
            "latest": .null
        ])

        guard let outboxState,
              case let .object(stateObject) = outboxState else {
            return defaultValue
        }

        let totalTickets = stateObject["totalTickets"] ?? .integer(0)
        let queuedTickets = stateObject["queuedTickets"] ?? .integer(0)
        let openTickets = stateObject["openTickets"] ?? .integer(0)
        let ackedTickets = stateObject["ackedTickets"] ?? .integer(0)

        let ticketObjects: [Object]
        if case let .list(list)? = stateObject["tickets"] {
            ticketObjects = list.compactMap { value in
                guard case let .object(object) = value else { return nil }
                return object
            }
        } else {
            ticketObjects = []
        }

        let items: ValueTypeList = ticketObjects.prefix(8).map { ticket in
            let payload: Object
            if case let .object(value)? = ticket["payload"] {
                payload = value
            } else {
                payload = [:]
            }

            let title = notificationStringValue(
                payload["title"] ??
                payload["headline"] ??
                payload["messageTitle"]
            ) ?? notificationStringValue(ticket["triggerEvent"]) ?? "Notification"
            let detail = notificationStringValue(
                payload["message"] ??
                payload["body"] ??
                payload["detail"]
            ) ?? notificationStringValue(ticket["requiredActionKey"]) ?? "Conference notification"
            let status = notificationStringValue(ticket["status"]) ?? "queued"
            let participantId = notificationStringValue(ticket["participantId"]) ?? ""
            let subtitle = participantId.isEmpty ? status : "\(status) · \(participantId)"

            return .object([
                "id": ticket["id"] ?? .string(UUID().uuidString),
                "title": .string(title),
                "subtitle": .string(subtitle),
                "detail": .string(detail),
                "status": .string(status),
                "createdAt": ticket["createdAt"] ?? .null
            ])
        }

        return .object([
            "connected": .bool(true),
            "totalTickets": totalTickets,
            "queuedTickets": queuedTickets,
            "openTickets": openTickets,
            "ackedTickets": ackedTickets,
            "items": .list(items),
            "latest": items.first ?? .null
        ])
    }

    private static func notificationSummaryValue(requester: Identity) async -> ValueType {
        guard let resolver = CellBase.defaultCellResolver,
              let cell = try? await resolver.cellAtEndpoint(
                endpoint: "cell:///NotificationOutbox",
                requester: requester
              ),
              let outbox = cell as? Meddle else {
            return notificationSummary(fromOutboxState: nil)
        }
        await ensurePortholeRuntimeBindingsIfNeeded(outbox, requester: requester)
        guard let outboxState = try? await outbox.get(keypath: "state", requester: requester) else {
            return notificationSummary(fromOutboxState: nil)
        }

        return notificationSummary(fromOutboxState: outboxState)
    }

    private static func notificationStringValue(_ value: ValueType?) -> String? {
        guard let value else { return nil }
        switch value {
        case .string(let string):
            let trimmed = string.trimmingCharacters(in: .whitespacesAndNewlines)
            return trimmed.isEmpty ? nil : trimmed
        default:
            return nil
        }
    }
}
