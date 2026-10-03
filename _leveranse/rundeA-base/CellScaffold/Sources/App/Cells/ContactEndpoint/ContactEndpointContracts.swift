// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

import Foundation
import CellBase

enum ContactEndpointContracts {
    static let cellName = "ContactEndpoint"
    static let endpoint = "cell:///ContactEndpoint"
    static let registryCellName = "ContactRegistry"
    static let registryEndpoint = "cell:///ContactRegistry"
    static let flowTopic = "cellprotocol.contact.endpoint"
    static let registryFlowTopic = "cellprotocol.contact.registry"
    static let requestSchema = "cellprotocol.contact.request.v1"
    static let descriptorSchema = "cellprotocol.contactEndpoint.descriptor.v1"
    static let proofSchema = "cellprotocol.contact.proof.v1"
    static let ticketSchema = "cellprotocol.contact.ticket.v1"
    static let requiredActionKey = "contact.ticket.review"
    static let notificationTriggerEvent = "contact.request.received"
    static let defaultTicketTTLSeconds = 15 * 60
    static let minimumTicketTTLSeconds = 60
    static let maximumTicketTTLSeconds = 24 * 60 * 60
    static let defaultEndpointTTLSeconds = 7 * 24 * 60 * 60
    static let maximumEndpointTTLSeconds = 366 * 24 * 60 * 60
    static let defaultMaxClockSkewSeconds = 5 * 60
    static let defaultPageLimit = 25
    static let maximumPageLimit = 100

    static func normalizedTTLSeconds(_ value: ValueType?, defaultValue: Int, maximum: Int) -> Int {
        let rawValue = intValue(value) ?? defaultValue
        return max(minimumTicketTTLSeconds, min(maximum, rawValue))
    }

    static func stringValue(_ value: ValueType?) -> String? {
        guard let value else { return nil }
        switch value {
        case .string(let string):
            let trimmed = string.trimmingCharacters(in: .whitespacesAndNewlines)
            return trimmed.isEmpty ? nil : trimmed
        default:
            return nil
        }
    }

    static func intValue(_ value: ValueType?) -> Int? {
        guard let value else { return nil }
        switch value {
        case .integer(let integer):
            return integer
        case .number(let number):
            return number
        case .float(let double):
            return Int(double)
        default:
            return nil
        }
    }

    static func boolValue(_ value: ValueType?) -> Bool? {
        guard case let .bool(bool)? = value else { return nil }
        return bool
    }

    static func objectValue(_ value: ValueType?) -> Object? {
        guard case let .object(object)? = value else { return nil }
        return object
    }

    static func listValue(_ value: ValueType?) -> [ValueType]? {
        guard case let .list(list)? = value else { return nil }
        return list
    }

    static func stringList(_ value: ValueType?) -> [String] {
        guard case let .list(list)? = value else { return [] }
        return list.compactMap { stringValue($0) }
    }

    static func dateValue(_ value: ValueType?) -> Date? {
        guard let value else { return nil }
        switch value {
        case .float(let timestamp):
            return Date(timeIntervalSince1970: timestamp)
        case .integer(let timestamp):
            return Date(timeIntervalSince1970: TimeInterval(timestamp))
        case .number(let timestamp):
            return Date(timeIntervalSince1970: TimeInterval(timestamp))
        case .string(let string):
            return ISO8601DateFormatter().date(from: string)
        default:
            return nil
        }
    }

    static func sha256Hex(_ data: Data) -> String {
        FlowHasher.sha256Hex(data)
    }

    static func sha256Hex(_ value: ValueType) -> String {
        guard let data = try? FlowCanonicalEncoder.canonicalData(for: .object(["value": value])) else {
            return sha256Hex(Data("serialization-error".utf8))
        }
        return sha256Hex(data)
    }

    static func normalizedHashRef(_ value: String) -> String {
        let trimmed = value.trimmingCharacters(in: .whitespacesAndNewlines)
        if trimmed.lowercased().hasPrefix("sha256:") {
            return trimmed
        }
        return "sha256:\(sha256Hex(Data(trimmed.utf8)))"
    }
}

enum ContactEndpointStatus: String, Codable, CaseIterable {
    case active
    case retired
    case expired
    case suspended
}

enum ContactTicketStatus: String, Codable, CaseIterable {
    case pending
    case delivered
    case resolved
    case accepted
    case declined
    case needsContract
    case blocked
    case expired
    case failed
}

enum ContactEndpointPolicyMode: String, Codable, CaseIterable {
    case openButFiltered
    case contractRequired
    case introductionOnly
    case knownRelationsOnly
    case ownerApprovalRequired
}

enum ContactProofRole: String, Codable, CaseIterable {
    case contextIssuer
    case registryPublisher
    case endpointOwner
    case custodian
    case requester
    case responder
}

struct ContactEndpointPolicy: Codable, Equatable {
    var mode: ContactEndpointPolicyMode
    var requireSignature: Bool
    var requireExpiry: Bool
    var allowedTopics: [String]
    var allowedPurposes: [String]
    var allowedActions: [String]
    var allowedDomains: [String]
    var blockedRequesterHashes: [String]
    var blockedDomains: [String]
    var allowPayloadBody: Bool
    var maxClockSkewSeconds: Int
    var maxPayloadCharacterCount: Int

    private enum CodingKeys: String, CodingKey {
        case mode
        case requireSignature
        case requireExpiry
        case allowedTopics
        case allowedPurposes
        case allowedActions
        case allowedDomains
        case blockedRequesterHashes
        case blockedDomains
        case allowPayloadBody
        case maxClockSkewSeconds
        case maxPayloadCharacterCount
    }

    static let `default` = ContactEndpointPolicy(
        mode: .ownerApprovalRequired,
        requireSignature: true,
        requireExpiry: true,
        allowedTopics: ["contact.request", "contact.message", "contact.consent"],
        allowedPurposes: ["purpose://contact.introduction", "purpose://contact.followup"],
        allowedActions: ["contact.request.submit"],
        allowedDomains: [],
        blockedRequesterHashes: [],
        blockedDomains: [],
        allowPayloadBody: true,
        maxClockSkewSeconds: ContactEndpointContracts.defaultMaxClockSkewSeconds,
        maxPayloadCharacterCount: 4096
    )

    init(
        mode: ContactEndpointPolicyMode,
        requireSignature: Bool,
        requireExpiry: Bool,
        allowedTopics: [String],
        allowedPurposes: [String],
        allowedActions: [String],
        allowedDomains: [String],
        blockedRequesterHashes: [String],
        blockedDomains: [String],
        allowPayloadBody: Bool,
        maxClockSkewSeconds: Int,
        maxPayloadCharacterCount: Int
    ) {
        self.mode = mode
        self.requireSignature = requireSignature
        self.requireExpiry = requireExpiry
        self.allowedTopics = allowedTopics
        self.allowedPurposes = allowedPurposes
        self.allowedActions = allowedActions
        self.allowedDomains = allowedDomains
        self.blockedRequesterHashes = blockedRequesterHashes
        self.blockedDomains = blockedDomains
        self.allowPayloadBody = allowPayloadBody
        self.maxClockSkewSeconds = max(0, maxClockSkewSeconds)
        self.maxPayloadCharacterCount = max(256, maxPayloadCharacterCount)
    }

    init(object: Object?) {
        guard let object else {
            self = .default
            return
        }
        let defaults = ContactEndpointPolicy.default
        self.init(
            mode: ContactEndpointPolicyMode(rawValue: ContactEndpointContracts.stringValue(object["mode"]) ?? "") ?? defaults.mode,
            requireSignature: ContactEndpointContracts.boolValue(object["requireSignature"]) ?? defaults.requireSignature,
            requireExpiry: ContactEndpointContracts.boolValue(object["requireExpiry"]) ?? defaults.requireExpiry,
            allowedTopics: ContactEndpointContracts.stringList(object["allowedTopics"]).nonEmpty ?? defaults.allowedTopics,
            allowedPurposes: ContactEndpointContracts.stringList(object["allowedPurposes"]).nonEmpty ?? defaults.allowedPurposes,
            allowedActions: ContactEndpointContracts.stringList(object["allowedActions"]).nonEmpty ?? defaults.allowedActions,
            allowedDomains: ContactEndpointContracts.stringList(object["allowedDomains"]),
            blockedRequesterHashes: ContactEndpointContracts.stringList(object["blockedRequesterHashes"]),
            blockedDomains: ContactEndpointContracts.stringList(object["blockedDomains"]),
            allowPayloadBody: ContactEndpointContracts.boolValue(object["allowPayloadBody"]) ?? defaults.allowPayloadBody,
            maxClockSkewSeconds: ContactEndpointContracts.intValue(object["maxClockSkewSeconds"]) ?? defaults.maxClockSkewSeconds,
            maxPayloadCharacterCount: ContactEndpointContracts.intValue(object["maxPayloadCharacterCount"]) ?? defaults.maxPayloadCharacterCount
        )
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        let defaults = ContactEndpointPolicy.default
        self.init(
            mode: try container.decodeIfPresent(ContactEndpointPolicyMode.self, forKey: .mode) ?? defaults.mode,
            requireSignature: try container.decodeIfPresent(Bool.self, forKey: .requireSignature) ?? defaults.requireSignature,
            requireExpiry: try container.decodeIfPresent(Bool.self, forKey: .requireExpiry) ?? defaults.requireExpiry,
            allowedTopics: try container.decodeIfPresent([String].self, forKey: .allowedTopics) ?? defaults.allowedTopics,
            allowedPurposes: try container.decodeIfPresent([String].self, forKey: .allowedPurposes) ?? defaults.allowedPurposes,
            allowedActions: try container.decodeIfPresent([String].self, forKey: .allowedActions) ?? defaults.allowedActions,
            allowedDomains: try container.decodeIfPresent([String].self, forKey: .allowedDomains) ?? defaults.allowedDomains,
            blockedRequesterHashes: try container.decodeIfPresent([String].self, forKey: .blockedRequesterHashes) ?? defaults.blockedRequesterHashes,
            blockedDomains: try container.decodeIfPresent([String].self, forKey: .blockedDomains) ?? defaults.blockedDomains,
            allowPayloadBody: try container.decodeIfPresent(Bool.self, forKey: .allowPayloadBody) ?? defaults.allowPayloadBody,
            maxClockSkewSeconds: try container.decodeIfPresent(Int.self, forKey: .maxClockSkewSeconds) ?? defaults.maxClockSkewSeconds,
            maxPayloadCharacterCount: try container.decodeIfPresent(Int.self, forKey: .maxPayloadCharacterCount) ?? defaults.maxPayloadCharacterCount
        )
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(mode, forKey: .mode)
        try container.encode(requireSignature, forKey: .requireSignature)
        try container.encode(requireExpiry, forKey: .requireExpiry)
        try container.encode(allowedTopics, forKey: .allowedTopics)
        try container.encode(allowedPurposes, forKey: .allowedPurposes)
        try container.encode(allowedActions, forKey: .allowedActions)
        try container.encode(allowedDomains, forKey: .allowedDomains)
        try container.encode(blockedRequesterHashes, forKey: .blockedRequesterHashes)
        try container.encode(blockedDomains, forKey: .blockedDomains)
        try container.encode(allowPayloadBody, forKey: .allowPayloadBody)
        try container.encode(maxClockSkewSeconds, forKey: .maxClockSkewSeconds)
        try container.encode(maxPayloadCharacterCount, forKey: .maxPayloadCharacterCount)
    }

    func publicObject() -> Object {
        [
            "mode": .string(mode.rawValue),
            "requireSignature": .bool(requireSignature),
            "requireExpiry": .bool(requireExpiry),
            "allowedTopics": .list(allowedTopics.map(ValueType.string)),
            "allowedPurposes": .list(allowedPurposes.map(ValueType.string)),
            "allowedActions": .list(allowedActions.map(ValueType.string)),
            "allowedDomains": .list(allowedDomains.map(ValueType.string)),
            "allowPayloadBody": .bool(allowPayloadBody),
            "maxClockSkewSeconds": .integer(maxClockSkewSeconds),
            "maxPayloadCharacterCount": .integer(maxPayloadCharacterCount)
        ]
    }

    func privateObject() -> Object {
        var object = publicObject()
        object["blockedRequesterHashes"] = .list(blockedRequesterHashes.map(ValueType.string))
        object["blockedDomains"] = .list(blockedDomains.map(ValueType.string))
        return object
    }
}

enum ContactProofChainVerifier {
    static func makeSignedProof(
        role: ContactProofRole,
        claim: String,
        subjectHash: String,
        signer: Identity,
        expiresAt: Date? = nil,
        now: Date = Date()
    ) async -> Object? {
        var proof: Object = [
            "schema": .string(ContactEndpointContracts.proofSchema),
            "role": .string(role.rawValue),
            "claim": .string(claim),
            "subjectHash": .string(subjectHash),
            "issuedAt": .float(now.timeIntervalSince1970),
            "signerIdentity": .identity(signer)
        ]
        proof["expiresAt"] = expiresAt.map { .float($0.timeIntervalSince1970) } ?? .null
        guard let data = try? FlowCanonicalEncoder.canonicalData(for: .object(proof)),
              let signature = try? await signer.sign(data: data) else {
            return nil
        }
        proof["signature"] = .data(signature)
        return proof
    }

    static func verifyProofChain(
        _ proofChain: [Object],
        requiredRoles: Set<ContactProofRole> = [],
        allowedRoles: Set<ContactProofRole> = Set(ContactProofRole.allCases),
        requiredSubjectHash: String? = nil,
        now: Date = Date()
    ) async -> Object {
        var verifiedRoles = Set<ContactProofRole>()
        var failures: [ValueType] = []

        for proof in proofChain {
            let result = await verifyProof(proof, allowedRoles: allowedRoles, requiredSubjectHash: requiredSubjectHash, now: now)
            if ContactEndpointContracts.boolValue(result["verified"]) == true,
               let roleString = ContactEndpointContracts.stringValue(result["role"]),
               let role = ContactProofRole(rawValue: roleString) {
                verifiedRoles.insert(role)
            } else {
                failures.append(.object(result))
            }
        }

        let missingRoles = requiredRoles.subtracting(verifiedRoles)
        let verified = failures.isEmpty && missingRoles.isEmpty
        return [
            "verified": .bool(verified),
            "status": .string(verified ? "verified" : (missingRoles.isEmpty ? "invalid_proof" : "missing_required_roles")),
            "proofCount": .integer(proofChain.count),
            "verifiedRoles": .list(verifiedRoles.sorted { $0.rawValue < $1.rawValue }.map { .string($0.rawValue) }),
            "missingRoles": .list(missingRoles.sorted { $0.rawValue < $1.rawValue }.map { .string($0.rawValue) }),
            "failures": .list(failures)
        ]
    }

    private static func verifyProof(
        _ proof: Object,
        allowedRoles: Set<ContactProofRole>,
        requiredSubjectHash: String?,
        now: Date
    ) async -> Object {
        guard ContactEndpointContracts.stringValue(proof["schema"]) ?? ContactEndpointContracts.proofSchema == ContactEndpointContracts.proofSchema else {
            return failure("unsupported_schema", role: ContactEndpointContracts.stringValue(proof["role"]))
        }
        guard let roleString = ContactEndpointContracts.stringValue(proof["role"]),
              let role = ContactProofRole(rawValue: roleString),
              allowedRoles.contains(role) else {
            return failure("unsupported_role", role: ContactEndpointContracts.stringValue(proof["role"]))
        }
        guard ContactEndpointContracts.stringValue(proof["claim"]) != nil,
              ContactEndpointContracts.stringValue(proof["subjectHash"]) != nil else {
            return failure("missing_claim_or_subject", role: roleString)
        }
        if let requiredSubjectHash,
           ContactEndpointContracts.stringValue(proof["subjectHash"]) != requiredSubjectHash {
            return failure("subject_mismatch", role: roleString)
        }
        if let issuedAt = ContactEndpointContracts.dateValue(proof["issuedAt"]),
           issuedAt.timeIntervalSince(now) > TimeInterval(ContactEndpointContracts.defaultMaxClockSkewSeconds) {
            return failure("issued_in_future", role: roleString)
        }
        if let expiresAt = ContactEndpointContracts.dateValue(proof["expiresAt"]),
           expiresAt < now {
            return failure("proof_expired", role: roleString)
        }
        guard case let .identity(identity)? = proof["signerIdentity"] else {
            return failure("missing_signer_identity", role: roleString)
        }
        guard let signature = signatureData(from: proof) else {
            return failure("missing_signature", role: roleString)
        }
        do {
            let data = try FlowCanonicalEncoder.canonicalData(for: .object(removingSignature(from: proof)))
            let verified = await identity.verify(signature: signature, for: data)
            return [
                "verified": .bool(verified),
                "status": .string(verified ? "verified" : "invalid_signature"),
                "role": .string(roleString),
                "signerHash": .string(ContactEndpointContracts.normalizedHashRef(identity.uuid))
            ]
        } catch {
            return failure("verification_error", role: roleString, message: "\(error)")
        }
    }

    private static func signatureData(from object: Object) -> Data? {
        if case let .data(data)? = object["signature"] {
            return data
        }
        if let encoded = ContactEndpointContracts.stringValue(object["signatureBase64"]) {
            return Data(base64Encoded: encoded)
        }
        return nil
    }

    private static func removingSignature(from object: Object) -> Object {
        var payload = object
        payload.removeValue(forKey: "signature")
        payload.removeValue(forKey: "signatureBase64")
        return payload
    }

    private static func failure(_ status: String, role: String?, message: String? = nil) -> Object {
        var object: Object = [
            "verified": .bool(false),
            "status": .string(status)
        ]
        object["role"] = role.map(ValueType.string) ?? .null
        object["message"] = message.map(ValueType.string) ?? .null
        return object
    }
}

struct ContactRouteRef: Codable, Equatable {
    var id: String
    var kind: String
    var cell: String?
    var topic: String?
    var participantId: String?
    var deviceId: String?
    var platform: String?
    var shardHint: String?
    var loadBalancerGroup: String?
    var lastSeenAt: Date?
    var expiresAt: Date?
    var revokedAt: Date?

    var isActive: Bool {
        revokedAt == nil && (expiresAt.map { $0 >= Date() } ?? true)
    }

    init(
        id: String = UUID().uuidString,
        kind: String,
        cell: String?,
        topic: String?,
        participantId: String?,
        deviceId: String?,
        platform: String?,
        shardHint: String?,
        loadBalancerGroup: String?,
        lastSeenAt: Date?,
        expiresAt: Date?,
        revokedAt: Date?
    ) {
        self.id = id
        self.kind = kind
        self.cell = cell
        self.topic = topic
        self.participantId = participantId
        self.deviceId = deviceId
        self.platform = platform
        self.shardHint = shardHint
        self.loadBalancerGroup = loadBalancerGroup
        self.lastSeenAt = lastSeenAt
        self.expiresAt = expiresAt
        self.revokedAt = revokedAt
    }

    init?(object: Object) {
        guard let kind = ContactEndpointContracts.stringValue(object["kind"]) else { return nil }
        self.init(
            id: ContactEndpointContracts.stringValue(object["id"]) ?? UUID().uuidString,
            kind: kind,
            cell: ContactEndpointContracts.stringValue(object["cell"]),
            topic: ContactEndpointContracts.stringValue(object["topic"]),
            participantId: ContactEndpointContracts.stringValue(object["participantId"]),
            deviceId: ContactEndpointContracts.stringValue(object["deviceId"]),
            platform: ContactEndpointContracts.stringValue(object["platform"]),
            shardHint: ContactEndpointContracts.stringValue(object["shardHint"]),
            loadBalancerGroup: ContactEndpointContracts.stringValue(object["loadBalancerGroup"]),
            lastSeenAt: ContactEndpointContracts.dateValue(object["lastSeenAt"]),
            expiresAt: ContactEndpointContracts.dateValue(object["expiresAt"]),
            revokedAt: ContactEndpointContracts.dateValue(object["revokedAt"])
        )
    }

    func privateObject() -> Object {
        var object: Object = [
            "id": .string(id),
            "kind": .string(kind),
            "isActive": .bool(isActive)
        ]
        object["cell"] = cell.map(ValueType.string) ?? .null
        object["topic"] = topic.map(ValueType.string) ?? .null
        object["participantId"] = participantId.map(ValueType.string) ?? .null
        object["deviceId"] = deviceId.map(ValueType.string) ?? .null
        object["platform"] = platform.map(ValueType.string) ?? .null
        object["shardHint"] = shardHint.map(ValueType.string) ?? .null
        object["loadBalancerGroup"] = loadBalancerGroup.map(ValueType.string) ?? .null
        object["lastSeenAt"] = lastSeenAt.map { .float($0.timeIntervalSince1970) } ?? .null
        object["expiresAt"] = expiresAt.map { .float($0.timeIntervalSince1970) } ?? .null
        object["revokedAt"] = revokedAt.map { .float($0.timeIntervalSince1970) } ?? .null
        return object
    }

    func publicSummaryObject() -> Object {
        var object: Object = [
            "id": .string(ContactEndpointContracts.normalizedHashRef(id)),
            "kind": .string(kind),
            "isActive": .bool(isActive)
        ]
        object["topic"] = topic.map(ValueType.string) ?? .null
        object["shardHint"] = shardHint.map(ValueType.string) ?? .null
        object["loadBalancerGroup"] = loadBalancerGroup.map(ValueType.string) ?? .null
        return object
    }
}

struct ContactEndpointRecord: Codable, Equatable {
    var endpointId: String
    var cell: String
    var ownerIdentityUUIDHash: String
    var ownerDomain: String?
    var status: ContactEndpointStatus
    var purposes: [String]
    var acceptedTopics: [String]
    var routingMode: String
    var contactSetIdHash: String?
    var contextRefs: [String]
    var policy: ContactEndpointPolicy
    var routeRefs: [ContactRouteRef]
    var proofChain: [Object]
    var custodyMode: String
    var custodianRef: Object?
    var retentionPurpose: String
    var discoverability: String
    var createdAt: Date
    var updatedAt: Date
    var expiresAt: Date?
    var ticketTTLSeconds: Int

    var isActive: Bool {
        status == .active && (expiresAt.map { $0 >= Date() } ?? true)
    }

    var ownerContextHash: String {
        ContactEndpointContracts.normalizedHashRef([
            "contact-endpoint-owner-context-v1",
            endpointId,
            cell,
            ownerIdentityUUIDHash,
            String(createdAt.timeIntervalSince1970)
        ].joined(separator: "::"))
    }

    func descriptorObject() -> Object {
        var descriptor: Object = [
            "schema": .string(ContactEndpointContracts.descriptorSchema),
            "endpointId": .string(endpointId),
            "cell": .string(cell),
            "ownerContextHash": .string(ownerContextHash),
            "purposes": .list(purposes.map(ValueType.string)),
            "acceptedTopics": .list(acceptedTopics.map(ValueType.string)),
            "routingMode": .string(routingMode),
            "contextRefs": .list(contextRefs.map(ValueType.string)),
            "custodyMode": .string(custodyMode),
            "retentionPurpose": .string(retentionPurpose),
            "discoverability": .string(discoverability),
            "createdAt": .float(createdAt.timeIntervalSince1970),
            "updatedAt": .float(updatedAt.timeIntervalSince1970),
            "status": .string(status.rawValue),
            "policy": .object(policy.publicObject())
        ]
        descriptor["ownerDomain"] = ownerDomain.map(ValueType.string) ?? .null
        descriptor["contactSetIdHash"] = contactSetIdHash.map(ValueType.string) ?? .null
        descriptor["custodianContextHash"] = custodianContextHash.map(ValueType.string) ?? .null
        descriptor["expiresAt"] = expiresAt.map { .float($0.timeIntervalSince1970) } ?? .null
        descriptor["descriptorHash"] = .string(descriptorHash)
        return descriptor
    }

    var descriptorHash: String {
        var descriptor = descriptorObjectWithoutHash()
        descriptor.removeValue(forKey: "descriptorHash")
        guard let data = try? FlowCanonicalEncoder.canonicalData(for: .object(descriptor)) else {
            return "sha256:\(ContactEndpointContracts.sha256Hex(Data(endpointId.utf8)))"
        }
        return "sha256:\(ContactEndpointContracts.sha256Hex(data))"
    }

    private func descriptorObjectWithoutHash() -> Object {
        var descriptor: Object = [
            "schema": .string(ContactEndpointContracts.descriptorSchema),
            "endpointId": .string(endpointId),
            "cell": .string(cell),
            "ownerContextHash": .string(ownerContextHash),
            "purposes": .list(purposes.map(ValueType.string)),
            "acceptedTopics": .list(acceptedTopics.map(ValueType.string)),
            "routingMode": .string(routingMode),
            "contextRefs": .list(contextRefs.map(ValueType.string)),
            "custodyMode": .string(custodyMode),
            "retentionPurpose": .string(retentionPurpose),
            "discoverability": .string(discoverability),
            "createdAt": .float(createdAt.timeIntervalSince1970),
            "updatedAt": .float(updatedAt.timeIntervalSince1970),
            "status": .string(status.rawValue),
            "policy": .object(policy.publicObject())
        ]
        descriptor["ownerDomain"] = ownerDomain.map(ValueType.string) ?? .null
        descriptor["contactSetIdHash"] = contactSetIdHash.map(ValueType.string) ?? .null
        descriptor["custodianContextHash"] = custodianContextHash.map(ValueType.string) ?? .null
        descriptor["expiresAt"] = expiresAt.map { .float($0.timeIntervalSince1970) } ?? .null
        return descriptor
    }

    func privateObject() -> Object {
        var object = descriptorObject()
        object["ownerIdentityUUIDHash"] = .string(ownerIdentityUUIDHash)
        object["policy"] = .object(policy.privateObject())
        object["routeRefs"] = .list(routeRefs.map { .object($0.privateObject()) })
        object["routeSummary"] = .object(routeSummaryObject())
        object["proofChain"] = .list(proofChain.map { .object($0) })
        object["custodianRef"] = custodianRef.map { .object($0) } ?? .null
        object["ticketTTLSeconds"] = .integer(ticketTTLSeconds)
        return object
    }

    func publicObject() -> Object {
        var object = descriptorObject()
        object["proofChainCount"] = .integer(proofChain.count)
        return object
    }

    private func routeSummaryObject() -> Object {
        let activeRoutes = routeRefs.filter(\.isActive)
        let loadBalancerGroups = Set(activeRoutes.compactMap(\.loadBalancerGroup)).sorted()
        return [
            "total": .integer(routeRefs.count),
            "active": .integer(activeRoutes.count),
            "kinds": .list(Array(Set(routeRefs.map(\.kind))).sorted().map(ValueType.string)),
            "loadBalancerGroups": .list(loadBalancerGroups.map(ValueType.string)),
            "publicRouteRefs": .list(activeRoutes.map { .object($0.publicSummaryObject()) })
        ]
    }

    private var custodianContextHash: String? {
        guard let custodianRef else { return nil }
        return ContactEndpointContracts.normalizedHashRef([
            "contact-endpoint-custodian-context-v1",
            endpointId,
            ContactEndpointContracts.sha256Hex(.object(custodianRef))
        ].joined(separator: "::"))
    }
}

struct ContactTicketRecord: Codable, Equatable {
    var ticketId: String
    var endpointId: String
    var status: ContactTicketStatus
    var requestTopic: String
    var purpose: String?
    var requesterIdentityHash: String
    var requesterDomain: String?
    var requestPayload: Object
    var correlationId: String?
    var notificationTicketId: String?
    var diagnosticMessage: String?
    var result: ValueType?
    var createdAt: Date
    var expiresAt: Date
    var resolvedAt: Date?
    var respondedAt: Date?

    func publicObject(includePayload: Bool = false) -> Object {
        var object: Object = [
            "schema": .string(ContactEndpointContracts.ticketSchema),
            "ticketId": .string(ticketId),
            "endpointId": .string(endpointId),
            "status": .string(status.rawValue),
            "requestTopic": .string(requestTopic),
            "requesterIdentityHash": .string(requesterIdentityHash),
            "createdAt": .float(createdAt.timeIntervalSince1970),
            "expiresAt": .float(expiresAt.timeIntervalSince1970)
        ]
        object["purpose"] = purpose.map(ValueType.string) ?? .null
        object["requesterDomain"] = requesterDomain.map(ValueType.string) ?? .null
        object["correlationId"] = correlationId.map(ValueType.string) ?? .null
        object["notificationTicketId"] = notificationTicketId.map(ValueType.string) ?? .null
        object["diagnosticMessage"] = diagnosticMessage.map(ValueType.string) ?? .null
        object["resolvedAt"] = resolvedAt.map { .float($0.timeIntervalSince1970) } ?? .null
        object["respondedAt"] = respondedAt.map { .float($0.timeIntervalSince1970) } ?? .null
        object["result"] = result ?? .null
        if includePayload {
            object["requestPayload"] = .object(requestPayload)
        }
        return object
    }
}

struct ContactRegistryEntry: Codable, Equatable {
    var entryId: String
    var registryId: String
    var endpointId: String
    var endpointCell: String
    var endpointDescriptor: Object
    var purposes: [String]
    var interests: [String]
    var contextRefs: [String]
    var visibility: String
    var discoverabilityContext: String
    var proofChain: [Object]
    var ownerIdentityHash: String?
    var shardKey: String
    var loadBalancerGroup: String?
    var status: String
    var createdAt: Date
    var updatedAt: Date
    var expiresAt: Date?

    var isActive: Bool {
        status == "active" && (expiresAt.map { $0 >= Date() } ?? true)
    }

    var entrySubjectHash: String {
        ContactEndpointContracts.normalizedHashRef([
            "contact-registry-entry-v1",
            registryId,
            entryId,
            endpointId,
            discoverabilityContext
        ].joined(separator: "::"))
    }

    var publisherContextHash: String? {
        ownerIdentityHash.map {
            ContactEndpointContracts.normalizedHashRef([
                "contact-registry-publisher-context-v1",
                registryId,
                entryId,
                discoverabilityContext,
                $0
            ].joined(separator: "::"))
        }
    }

    func publicObject() -> Object {
        var object: Object = [
            "entryId": .string(entryId),
            "registryId": .string(registryId),
            "endpointId": .string(endpointId),
            "endpointCell": .string(endpointCell),
            "endpointDescriptor": .object(endpointDescriptor),
            "purposes": .list(purposes.map(ValueType.string)),
            "interests": .list(interests.map(ValueType.string)),
            "contextRefs": .list(contextRefs.map(ValueType.string)),
            "visibility": .string(visibility),
            "discoverabilityContext": .string(discoverabilityContext),
            "proofChainCount": .integer(proofChain.count),
            "shardKey": .string(shardKey),
            "status": .string(status),
            "createdAt": .float(createdAt.timeIntervalSince1970),
            "updatedAt": .float(updatedAt.timeIntervalSince1970)
        ]
        object["publisherContextHash"] = publisherContextHash.map(ValueType.string) ?? .null
        object["loadBalancerGroup"] = loadBalancerGroup.map(ValueType.string) ?? .null
        object["expiresAt"] = expiresAt.map { .float($0.timeIntervalSince1970) } ?? .null
        return object
    }

    func privateObject() -> Object {
        var object = publicObject()
        object["ownerIdentityHash"] = ownerIdentityHash.map(ValueType.string) ?? .null
        object["proofChain"] = .list(proofChain.map { .object($0) })
        return object
    }
}

private extension Array {
    var nonEmpty: [Element]? {
        isEmpty ? nil : self
    }
}
