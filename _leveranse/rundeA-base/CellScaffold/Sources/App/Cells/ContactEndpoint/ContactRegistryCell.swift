// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

import Foundation
import CellBase

final class ContactRegistryCell: GeneralCell {
    enum CodingKeys: CodingKey {
        case generalCell
        case owner
        case entriesByID
    }

    private let stateQueue = DispatchQueue(label: "ContactRegistryCell.State")
    private var entriesByID: [String: ContactRegistryEntry]

    required init(owner: Identity) async {
        self.entriesByID = [:]
        await super.init(owner: owner)
        await setupPermissions(owner: owner)
        await setupKeys(owner: owner)
    }

    required init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.entriesByID = (try? container.decode([String: ContactRegistryEntry].self, forKey: .entriesByID)) ?? [:]
        try super.init(from: decoder)

        if let owner = try? container.decodeIfPresent(Identity.self, forKey: .owner) {
            Task {
                await self.setupPermissions(owner: owner)
                await self.setupKeys(owner: owner)
            }
        }
    }

    override func encode(to encoder: Encoder) throws {
        try super.encode(to: encoder)
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(stateQueue.sync { entriesByID }, forKey: .entriesByID)
    }

    private func setupPermissions(owner: Identity) async {
        agreementTemplate.addGrant("r---", for: "state")
        agreementTemplate.addGrant("rw--", for: "publishEntry")
        agreementTemplate.addGrant("rw--", for: "retireEntry")
        agreementTemplate.addGrant("rw--", for: "search")
        agreementTemplate.addGrant("rw--", for: "expire")
        agreementTemplate.addGrant("r---", for: "feed")
    }

    private func setupKeys(owner: Identity) async {
        await addInterceptForGet(requester: owner, key: "state", getValueIntercept: { [weak self] _, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("r---", at: "state", for: requester) else { return .string("denied") }
            return self.stateValue()
        })

        await addInterceptForSet(requester: owner, key: "publishEntry", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "publishEntry", for: requester) else { return .string("denied") }
            guard case let .object(object) = value else {
                return .object(self.error("expected_object", "publishEntry expects an object payload."))
            }
            guard var entry = self.entry(from: object, requester: requester) else {
                return .object(self.error("invalid_entry", "Entry must include endpointDescriptor, endpointId, purposes/interests, and discoverabilityContext."))
            }
            if entry.proofChain.isEmpty,
               let proof = await ContactProofChainVerifier.makeSignedProof(
                    role: .registryPublisher,
                    claim: "publisher actively placed endpoint descriptor in registry context",
                    subjectHash: entry.entrySubjectHash,
                    signer: requester,
                    expiresAt: entry.expiresAt
               ) {
                entry.proofChain.append(proof)
            }
            let proofVerification = await ContactProofChainVerifier.verifyProofChain(
                entry.proofChain,
                requiredRoles: [.registryPublisher],
                requiredSubjectHash: entry.entrySubjectHash,
                now: Date()
            )
            guard ContactEndpointContracts.boolValue(proofVerification["verified"]) == true else {
                return .object([
                    "status": .string("error"),
                    "code": .string("proof_chain_invalid"),
                    "message": .string("Registry entry proof chain is missing or invalid."),
                    "verification": .object(proofVerification)
                ])
            }
            self.stateQueue.sync {
                self.entriesByID[entry.entryId] = entry
            }
            await self.emitEvent("contact.registry.entry.published", payload: entry.publicObject(), requester: requester)
            return .object(entry.publicObject())
        })

        await addInterceptForSet(requester: owner, key: "retireEntry", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "retireEntry", for: requester) else { return .string("denied") }
            guard let entryId = Self.entryId(from: value) else {
                return .object(self.error("missing_entry_id", "retireEntry expects entryId."))
            }
            guard let entry = self.retireEntry(entryId: entryId) else {
                return .object(self.error("not_found", "Registry entry not found."))
            }
            await self.emitEvent("contact.registry.entry.retired", payload: entry.publicObject(), requester: requester)
            return .object(entry.publicObject())
        })

        await addInterceptForSet(requester: owner, key: "search", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "search", for: requester) else { return .string("denied") }
            guard case let .object(object) = value else {
                return .object(self.error("expected_object", "search expects an object payload."))
            }
            let result = self.search(object)
            await self.emitEvent("contact.registry.search", payload: result, requester: requester)
            return .object(result)
        })

        await addInterceptForSet(requester: owner, key: "expire", setValueIntercept: { [weak self] _, _, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "expire", for: requester) else { return .string("denied") }
            let result = self.expireStaleEntries()
            await self.emitEvent("contact.registry.expire.sweep", payload: result, requester: requester)
            return .object(result)
        })
    }

    private func stateValue() -> ValueType {
        let snapshot = stateQueue.sync { entriesByID.values.sorted { $0.updatedAt > $1.updatedAt } }
        return .object([
            "cell": .string(ContactEndpointContracts.registryEndpoint),
            "entryCount": .integer(snapshot.count),
            "activeEntryCount": .integer(snapshot.filter(\.isActive).count),
            "entries": .list(snapshot.map { .object($0.publicObject()) }),
            "scaling": .object([
                "pageLimitDefault": .integer(ContactEndpointContracts.defaultPageLimit),
                "pageLimitMaximum": .integer(ContactEndpointContracts.maximumPageLimit),
                "sharding": .string("MVP stores entries in one cell but every entry carries shardKey/loadBalancerGroup for federation or partitioning.")
            ])
        ])
    }

    private func entry(from object: Object, requester: Identity) -> ContactRegistryEntry? {
        guard let rawDescriptor = ContactEndpointContracts.objectValue(object["endpointDescriptor"]),
              let descriptor = Self.publicSafeDescriptor(from: rawDescriptor),
              let endpointId = ContactEndpointContracts.stringValue(object["endpointId"])
                ?? ContactEndpointContracts.stringValue(descriptor["endpointId"]),
              let endpointCell = ContactEndpointContracts.stringValue(object["endpointCell"])
                ?? ContactEndpointContracts.stringValue(descriptor["cell"]) else {
            return nil
        }
        let purposes = ContactEndpointContracts.stringList(object["purposes"]).nonEmpty
            ?? ContactEndpointContracts.stringList(descriptor["purposes"])
        let interests = ContactEndpointContracts.stringList(object["interests"])
        guard purposes.isEmpty == false || interests.isEmpty == false else {
            return nil
        }
        guard let discoverabilityContext = ContactEndpointContracts.stringValue(object["discoverabilityContext"]) else {
            return nil
        }
        let now = Date()
        let proofChain = ContactEndpointContracts.listValue(object["proofChain"])?
            .compactMap(ContactEndpointContracts.objectValue) ?? []
        let entryId = ContactEndpointContracts.stringValue(object["entryId"]) ?? "contact-registry-\(UUID().uuidString.lowercased())"
        let ownerRef = ContactEndpointContracts.stringValue(object["ownerIdentityRef"]) ?? requester.uuid
        let expiresAt = ContactEndpointContracts.dateValue(object["expiresAt"])
            ?? ContactEndpointContracts.dateValue(descriptor["expiresAt"])
            ?? now.addingTimeInterval(TimeInterval(ContactEndpointContracts.defaultEndpointTTLSeconds))
        let shardMaterial = [
            ContactEndpointContracts.stringValue(object["registryId"]) ?? "default",
            discoverabilityContext,
            endpointId,
            purposes.joined(separator: ","),
            interests.joined(separator: ",")
        ].joined(separator: "::")

        return ContactRegistryEntry(
            entryId: entryId,
            registryId: ContactEndpointContracts.stringValue(object["registryId"]) ?? "default",
            endpointId: endpointId,
            endpointCell: endpointCell,
            endpointDescriptor: descriptor,
            purposes: purposes,
            interests: interests,
            contextRefs: ContactEndpointContracts.stringList(object["contextRefs"]),
            visibility: ContactEndpointContracts.stringValue(object["visibility"]) ?? "members",
            discoverabilityContext: discoverabilityContext,
            proofChain: proofChain,
            ownerIdentityHash: ContactEndpointContracts.normalizedHashRef(ownerRef),
            shardKey: ContactEndpointContracts.stringValue(object["shardKey"])
                ?? String(ContactEndpointContracts.sha256Hex(Data(shardMaterial.utf8)).prefix(16)),
            loadBalancerGroup: ContactEndpointContracts.stringValue(object["loadBalancerGroup"]),
            status: "active",
            createdAt: now,
            updatedAt: now,
            expiresAt: expiresAt
        )
    }

    private static func publicSafeDescriptor(from descriptor: Object) -> Object? {
        let forbiddenKeys = [
            "routeRefs",
            "routeSummary",
            "ownerIdentityUUIDHash",
            "ownerIdentityHash",
            "ownerIdentityRef",
            "participantId",
            "deviceId",
            "pushToken",
            "pushEndpoint",
            "registrationToken",
            "bridgeSessionId",
            "activeBridgeId",
            "proofChain"
        ]
        guard forbiddenKeys.allSatisfy({ descriptor[$0] == nil }) else {
            return nil
        }
        return descriptor
    }

    private func retireEntry(entryId: String) -> ContactRegistryEntry? {
        stateQueue.sync {
            guard var entry = entriesByID[entryId] else { return nil }
            entry.status = "retired"
            entry.updatedAt = Date()
            entriesByID[entryId] = entry
            return entry
        }
    }

    private func search(_ object: Object) -> Object {
        let requestedPurpose = ContactEndpointContracts.stringValue(object["purpose"])
        let requestedInterests = Set(ContactEndpointContracts.stringList(object["interests"]).map { $0.lowercased() })
        let requestedContext = ContactEndpointContracts.stringValue(object["contextRef"])
        let registryId = ContactEndpointContracts.stringValue(object["registryId"])
        let limit = max(1, min(
            ContactEndpointContracts.maximumPageLimit,
            ContactEndpointContracts.intValue(object["limit"]) ?? ContactEndpointContracts.defaultPageLimit
        ))
        let offset = max(0, ContactEndpointContracts.intValue(object["offset"]) ?? 0)
        let now = Date()

        let matches = stateQueue.sync {
            entriesByID.values.compactMap { entry -> (ContactRegistryEntry, Int)? in
                guard entry.isActive,
                      entry.expiresAt.map({ $0 >= now }) ?? true,
                      entry.visibility != "private" else {
                    return nil
                }
                if let registryId, entry.registryId != registryId {
                    return nil
                }
                var score = 0
                if let requestedPurpose {
                    if entry.purposes.contains(requestedPurpose) {
                        score += 4
                    } else {
                        return nil
                    }
                }
                if requestedInterests.isEmpty == false {
                    let entryInterests = Set(entry.interests.map { $0.lowercased() })
                    let overlap = requestedInterests.intersection(entryInterests).count
                    guard overlap > 0 else {
                        return nil
                    }
                    score += overlap
                }
                if let requestedContext {
                    if entry.contextRefs.contains(requestedContext) || entry.discoverabilityContext == requestedContext {
                        score += 2
                    } else {
                        return nil
                    }
                }
                return (entry, score)
            }
            .sorted { lhs, rhs in
                if lhs.1 != rhs.1 {
                    return lhs.1 > rhs.1
                }
                return lhs.0.updatedAt > rhs.0.updatedAt
            }
        }

        let page = Array(matches.dropFirst(offset).prefix(limit))
        return [
            "status": .string("ok"),
            "totalMatches": .integer(matches.count),
            "offset": .integer(offset),
            "limit": .integer(limit),
            "results": .list(page.map { entry, score in
                var object = entry.publicObject()
                object["score"] = .integer(score)
                return .object(object)
            }),
            "scaling": .object([
                "nextOffset": .integer(offset + page.count),
                "hasMore": .bool(offset + page.count < matches.count),
                "shardKeys": .list(Array(Set(page.map { $0.0.shardKey })).sorted().map(ValueType.string))
            ])
        ]
    }

    private func expireStaleEntries(now: Date = Date()) -> Object {
        stateQueue.sync {
            var expiredCount = 0
            for (entryId, var entry) in entriesByID where entry.status == "active" {
                if let expiresAt = entry.expiresAt, expiresAt < now {
                    entry.status = "expired"
                    entry.updatedAt = now
                    entriesByID[entryId] = entry
                    expiredCount += 1
                }
            }
            return [
                "expiredCount": .integer(expiredCount),
                "timestamp": .float(now.timeIntervalSince1970)
            ]
        }
    }

    private func emitEvent(_ title: String, payload: Object, requester: Identity) async {
        var flowElement = FlowElement(
            title: title,
            content: .object(payload),
            properties: FlowElement.Properties(type: .event, contentType: .object)
        )
        flowElement.topic = ContactEndpointContracts.registryFlowTopic
        flowElement.origin = uuid
        pushFlowElement(flowElement, requester: requester)
    }

    private func error(_ code: String, _ message: String) -> Object {
        [
            "status": .string("error"),
            "code": .string(code),
            "message": .string(message)
        ]
    }

    private static func entryId(from value: ValueType) -> String? {
        switch value {
        case .string(let entryId):
            return entryId.trimmingCharacters(in: .whitespacesAndNewlines).nonEmpty
        case .object(let object):
            return ContactEndpointContracts.stringValue(object["entryId"])
        default:
            return nil
        }
    }
}

private extension String {
    var nonEmpty: String? {
        isEmpty ? nil : self
    }
}

private extension Array {
    var nonEmpty: [Element]? {
        isEmpty ? nil : self
    }
}
