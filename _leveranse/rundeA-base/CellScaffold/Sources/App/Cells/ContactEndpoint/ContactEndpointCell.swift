// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

import Foundation
import CellBase

final class ContactEndpointCell: GeneralCell, PortholeRuntimeBindingEnsuring {
    enum CodingKeys: CodingKey {
        case generalCell
        case owner
        case endpointsByID
        case ticketsByID
        case seenNonces
    }

    private let stateQueue = DispatchQueue(label: "ContactEndpointCell.State")
    private var endpointsByID: [String: ContactEndpointRecord]
    private var ticketsByID: [String: ContactTicketRecord]
    private var seenNonces: [String: Date]
    private let nowProvider: @Sendable () -> Date

    private enum TicketMutation {
        case success(ContactTicketRecord, didTransition: Bool)
        case failure(code: String, message: String)
    }

    required init(owner: Identity) async {
        self.endpointsByID = [:]
        self.ticketsByID = [:]
        self.seenNonces = [:]
        self.nowProvider = { Date() }
        await super.init(owner: owner)
        configureAgreementTemplate()
        await setupRuntimeBindings(owner: owner)
    }

    init(
        owner: Identity,
        nowProvider: @escaping @Sendable () -> Date
    ) async {
        self.endpointsByID = [:]
        self.ticketsByID = [:]
        self.seenNonces = [:]
        self.nowProvider = nowProvider
        await super.init(owner: owner)
        configureAgreementTemplate()
        await setupRuntimeBindings(owner: owner)
    }

    required init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.endpointsByID = (try? container.decode([String: ContactEndpointRecord].self, forKey: .endpointsByID)) ?? [:]
        self.ticketsByID = (try? container.decode([String: ContactTicketRecord].self, forKey: .ticketsByID)) ?? [:]
        self.seenNonces = (try? container.decode([String: Date].self, forKey: .seenNonces)) ?? [:]
        self.nowProvider = { Date() }
        try super.init(from: decoder)
    }

    override func encode(to encoder: Encoder) throws {
        try super.encode(to: encoder)
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(stateQueue.sync { endpointsByID }, forKey: .endpointsByID)
        try container.encode(stateQueue.sync { ticketsByID }, forKey: .ticketsByID)
        try container.encode(stateQueue.sync { seenNonces }, forKey: .seenNonces)
    }

    func ensurePortholeRuntimeBindings(requester: Identity) async {
        let owner = await portholeRuntimeOwner(requester: requester)
        await setupRuntimeBindings(owner: owner)
    }

    private func setupRuntimeBindings(owner: Identity) async {
        await installPortholeRuntimeBindings(
            owner: owner,
            installPermissions: { _ in },
            installRuntime: { [weak self] owner in
                await self?.setupKeys(owner: owner)
            }
        )
    }

    private func configureAgreementTemplate() {
        agreementTemplate.addGrant("r---", for: "state")
        agreementTemplate.addGrant("r---", for: "privateState")
        agreementTemplate.addGrant("rw--", for: "publishEndpoint")
        agreementTemplate.addGrant("rw--", for: "retireEndpoint")
        agreementTemplate.addGrant("rw--", for: "contact.request")
        agreementTemplate.addGrant("rw--", for: "ticket.resolve")
        agreementTemplate.addGrant("rw--", for: "ticket.respond")
        agreementTemplate.addGrant("rw--", for: "device.resolveTicket")
        agreementTemplate.addGrant("rw--", for: "device.submitTicketResult")
        agreementTemplate.addGrant("rw--", for: "route.heartbeat")
        agreementTemplate.addGrant("rw--", for: "route.revoke")
        agreementTemplate.addGrant("rw--", for: "expire")
        agreementTemplate.addGrant("r---", for: "feed")
    }

    private func setupKeys(owner: Identity) async {
        await addInterceptForGet(requester: owner, key: "state", getValueIntercept: { [weak self] _, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("r---", at: "state", for: requester) else { return .string("denied") }
            return self.stateValue(includePrivate: false)
        })

        await addInterceptForGet(requester: owner, key: "privateState", getValueIntercept: { [weak self] _, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("r---", at: "privateState", for: requester) else { return .string("denied") }
            return self.stateValue(includePrivate: true)
        })

        await addInterceptForSet(requester: owner, key: "publishEndpoint", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "publishEndpoint", for: requester) else { return .string("denied") }
            guard case let .object(object) = value else {
                return .object(self.error("expected_object", "publishEndpoint expects an object payload."))
            }
            let publication = await self.publishEndpoint(from: object, requester: requester)
            if let error = publication.error {
                return .object(error)
            }
            guard let record = publication.record else {
                return .object(self.error("publish_failed", "Endpoint publication failed."))
            }
            await self.emitEvent("contact.endpoint.published", payload: record.publicObject(), requester: requester)
            await self.persistEndpointPublicationIfRequested(record: record, payload: object, requester: requester)
            return .object(record.publicObject())
        })

        await addInterceptForSet(requester: owner, key: "retireEndpoint", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "retireEndpoint", for: requester) else { return .string("denied") }
            guard let endpointId = Self.endpointId(from: value) else {
                return .object(self.error("missing_endpoint_id", "retireEndpoint expects endpointId."))
            }
            guard let record = self.updateEndpointStatus(endpointId: endpointId, status: .retired) else {
                return .object(self.error("not_found", "Endpoint not found."))
            }
            await self.emitEvent("contact.endpoint.retired", payload: record.publicObject(), requester: requester)
            return .object(record.publicObject())
        })

        await addInterceptForSet(requester: owner, key: "contact.request", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "contact.request", for: requester) else { return .string("denied") }
            guard case let .object(object) = value else {
                return .object(self.error("expected_object", "contact.request expects an object payload."))
            }
            let result = await self.handleContactRequest(object, requester: requester)
            return .object(result)
        })

        await addInterceptForSet(requester: owner, key: "ticket.resolve", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "ticket.resolve", for: requester) else { return .string("denied") }
            guard let ticketId = Self.ticketId(from: value) else {
                return .object(self.error("missing_ticket_id", "ticket.resolve expects ticketId."))
            }
            return .object(await self.resolveTicket(ticketId: ticketId, requester: requester))
        })

        await addInterceptForSet(requester: owner, key: "ticket.respond", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "ticket.respond", for: requester) else { return .string("denied") }
            guard case let .object(object) = value,
                  let ticketId = ContactEndpointContracts.stringValue(object["ticketId"]) else {
                return .object(self.error("missing_ticket_id", "ticket.respond expects ticketId."))
            }
            return .object(await self.respondTicket(ticketId: ticketId, payload: object, requester: requester))
        })

        await addInterceptForSet(requester: owner, key: "device.resolveTicket", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "device.resolveTicket", for: requester) else { return .string("denied") }
            guard case let .object(object) = value,
                  let ticketId = ContactEndpointContracts.stringValue(object["ticketId"]) else {
                return .object(self.error("missing_ticket_id", "device.resolveTicket expects ticketId."))
            }
            guard self.deviceRouteAllowsCallback(payload: object) else {
                return .object(self.error("device_route_not_allowed", "No matching active private route allows this device callback."))
            }
            return .object(await self.resolveTicket(ticketId: ticketId, requester: requester))
        })

        await addInterceptForSet(requester: owner, key: "device.submitTicketResult", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "device.submitTicketResult", for: requester) else { return .string("denied") }
            guard case let .object(object) = value,
                  let ticketId = ContactEndpointContracts.stringValue(object["ticketId"]) else {
                return .object(self.error("missing_ticket_id", "device.submitTicketResult expects ticketId."))
            }
            guard self.deviceRouteAllowsCallback(payload: object) else {
                return .object(self.error("device_route_not_allowed", "No matching active private route allows this device callback."))
            }
            return .object(await self.respondTicket(ticketId: ticketId, payload: object, requester: requester))
        })

        await addInterceptForSet(requester: owner, key: "route.heartbeat", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "route.heartbeat", for: requester) else { return .string("denied") }
            guard case let .object(object) = value,
                  let endpointId = ContactEndpointContracts.stringValue(object["endpointId"]) else {
                return .object(self.error("missing_endpoint_id", "route.heartbeat expects endpointId."))
            }
            guard let updated = self.upsertRoute(endpointId: endpointId, payload: object) else {
                return .object(self.error("not_found", "Endpoint not found."))
            }
            await self.emitEvent("contact.route.heartbeat", payload: updated.publicObject(), requester: requester)
            return .object(updated.privateObject())
        })

        await addInterceptForSet(requester: owner, key: "route.revoke", setValueIntercept: { [weak self] _, value, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "route.revoke", for: requester) else { return .string("denied") }
            guard case let .object(object) = value,
                  let endpointId = ContactEndpointContracts.stringValue(object["endpointId"]),
                  let routeId = ContactEndpointContracts.stringValue(object["routeId"]) else {
                return .object(self.error("missing_route_ref", "route.revoke expects endpointId and routeId."))
            }
            guard let updated = self.revokeRoute(endpointId: endpointId, routeId: routeId) else {
                return .object(self.error("not_found", "Endpoint or route not found."))
            }
            await self.emitEvent("contact.route.revoked", payload: updated.publicObject(), requester: requester)
            return .object(updated.privateObject())
        })

        await addInterceptForSet(requester: owner, key: "expire", setValueIntercept: { [weak self] _, _, requester in
            guard let self else { return .string("failure") }
            guard await self.validateAccess("rw--", at: "expire", for: requester) else { return .string("denied") }
            let result = self.expireStaleRecords()
            await self.emitEvent("contact.expire.sweep", payload: result, requester: requester)
            return .object(result)
        })
    }

    private func stateValue(includePrivate: Bool) -> ValueType {
        let snapshot = stateQueue.sync {
            (
                endpoints: endpointsByID.values.sorted { $0.updatedAt > $1.updatedAt },
                tickets: ticketsByID.values.sorted { $0.createdAt > $1.createdAt },
                nonceCount: seenNonces.count
            )
        }
        let activeEndpoints = snapshot.endpoints.filter(\.isActive)
        let pendingTickets = snapshot.tickets.filter { $0.status == .pending || $0.status == .delivered || $0.status == .resolved }
        return .object([
            "cell": .string(ContactEndpointContracts.endpoint),
            "endpointCount": .integer(snapshot.endpoints.count),
            "activeEndpointCount": .integer(activeEndpoints.count),
            "ticketCount": .integer(snapshot.tickets.count),
            "pendingTicketCount": .integer(pendingTickets.count),
            "seenNonceCount": .integer(snapshot.nonceCount),
            "endpoints": .list(snapshot.endpoints.map { .object(includePrivate ? $0.privateObject() : $0.publicObject()) }),
            "tickets": .list(snapshot.tickets.map { .object($0.publicObject(includePayload: includePrivate)) })
        ])
    }

    private func publishEndpoint(from object: Object, requester: Identity) async -> (record: ContactEndpointRecord?, error: Object?) {
        let now = nowProvider()
        let endpointId = ContactEndpointContracts.stringValue(object["endpointId"]) ?? "contact-\(UUID().uuidString.lowercased())"
        guard isSupportedEndpointCellAddress(ContactEndpointContracts.stringValue(object["cell"]) ?? ContactEndpointContracts.endpoint) else {
            return (nil, error("unsupported_cell_path", "ContactEndpoint uses one routable cell address and carries endpointId in the payload."))
        }
        if let custodyError = validateCustodyPayload(object) {
            return (nil, custodyError)
        }
        let ttlSeconds = ContactEndpointContracts.normalizedTTLSeconds(
            object["endpointTTLSeconds"] ?? object["ttlSeconds"],
            defaultValue: ContactEndpointContracts.defaultEndpointTTLSeconds,
            maximum: ContactEndpointContracts.maximumEndpointTTLSeconds
        )
        let explicitExpiresAt = ContactEndpointContracts.dateValue(object["expiresAt"])
        let expiresAt = explicitExpiresAt ?? now.addingTimeInterval(TimeInterval(ttlSeconds))
        let purposes = ContactEndpointContracts.stringList(object["purposes"]).nonEmpty ?? ContactEndpointPolicy.default.allowedPurposes
        let acceptedTopics = ContactEndpointContracts.stringList(object["acceptedTopics"]).nonEmpty ?? ContactEndpointPolicy.default.allowedTopics
        let contactSetId = ContactEndpointContracts.stringValue(object["contactSetId"])
        let ownerIdentityRef = ContactEndpointContracts.stringValue(object["ownerIdentityRef"]) ?? requester.uuid
        let proofChain = ContactEndpointContracts.listValue(object["proofChain"])?
            .compactMap(ContactEndpointContracts.objectValue) ?? []
        let routeRefs = ContactEndpointContracts.listValue(object["routeRefs"])?
            .compactMap(ContactEndpointContracts.objectValue)
            .compactMap(ContactRouteRef.init(object:)) ?? []
        let cellAddress = ContactEndpointContracts.stringValue(object["cell"]) ?? ContactEndpointContracts.endpoint

        var record = ContactEndpointRecord(
            endpointId: endpointId,
            cell: cellAddress,
            ownerIdentityUUIDHash: ContactEndpointContracts.normalizedHashRef(ownerIdentityRef),
            ownerDomain: ContactEndpointContracts.stringValue(object["ownerDomain"]),
            status: .active,
            purposes: purposes,
            acceptedTopics: acceptedTopics,
            routingMode: ContactEndpointContracts.stringValue(object["routingMode"]) ?? (contactSetId == nil ? "direct" : "opaqueSetRouter"),
            contactSetIdHash: contactSetId.map {
                ContactEndpointContracts.normalizedHashRef([
                    "contact-endpoint-set-context-v1",
                    endpointId,
                    $0,
                    String(now.timeIntervalSince1970)
                ].joined(separator: "::"))
            },
            contextRefs: ContactEndpointContracts.stringList(object["contextRefs"]),
            policy: ContactEndpointPolicy(object: ContactEndpointContracts.objectValue(object["policy"])),
            routeRefs: routeRefs,
            proofChain: proofChain,
            custodyMode: ContactEndpointContracts.stringValue(object["custodyMode"]) ?? "userControlledVault",
            custodianRef: sanitizedCustodianRef(from: object),
            retentionPurpose: ContactEndpointContracts.stringValue(object["retentionPurpose"]) ?? "temporary-contact",
            discoverability: ContactEndpointContracts.stringValue(object["discoverability"]) ?? "private",
            createdAt: now,
            updatedAt: now,
            expiresAt: expiresAt,
            ticketTTLSeconds: ContactEndpointContracts.normalizedTTLSeconds(
                object["ticketTTLSeconds"],
                defaultValue: ContactEndpointContracts.defaultTicketTTLSeconds,
                maximum: ContactEndpointContracts.maximumTicketTTLSeconds
            )
        )

        if record.proofChain.isEmpty,
           let proof = await ContactProofChainVerifier.makeSignedProof(
                role: .endpointOwner,
                claim: "endpoint owner authorized contact endpoint publication",
                subjectHash: record.descriptorHash,
                signer: requester,
                now: now
           ) {
            record.proofChain.append(proof)
        }
        let requiredRoles = requiredProofRoles(for: object, record: record)
        let proofVerification = await ContactProofChainVerifier.verifyProofChain(
            record.proofChain,
            requiredRoles: requiredRoles,
            requiredSubjectHash: record.descriptorHash,
            now: now
        )
        guard ContactEndpointContracts.boolValue(proofVerification["verified"]) == true else {
            return (nil, [
                "status": .string("error"),
                "code": .string("proof_chain_invalid"),
                "message": .string("Endpoint proof chain is missing or invalid."),
                "verification": .object(proofVerification)
            ])
        }

        stateQueue.sync {
            endpointsByID[endpointId] = record
        }
        return (record, nil)
    }

    private func handleContactRequest(_ object: Object, requester: Identity) async -> Object {
        let now = nowProvider()
        guard ContactEndpointContracts.stringValue(object["schema"]) ?? ContactEndpointContracts.requestSchema == ContactEndpointContracts.requestSchema else {
            return error("unsupported_schema", "Unsupported contact request schema.")
        }
        guard let endpointId = ContactEndpointContracts.stringValue(object["endpointId"]) else {
            return error("missing_endpoint_id", "Contact request is missing endpointId.")
        }
        guard let endpoint = endpointSnapshot(endpointId: endpointId) else {
            return error("not_found", "Endpoint not found.")
        }
        guard endpoint.status == .active else {
            return error("endpoint_not_active", "Endpoint is \(endpoint.status.rawValue).")
        }
        guard endpoint.expiresAt.map({ now <= $0 }) ?? true else {
            _ = updateEndpointStatus(endpointId: endpointId, status: .expired)
            return error("endpoint_expired", "Endpoint has expired.")
        }
        guard let nonce = ContactEndpointContracts.stringValue(object["nonce"]) else {
            return error("missing_nonce", "Contact request is missing nonce.")
        }
        guard let topic = ContactEndpointContracts.stringValue(object["topic"]) else {
            return error("missing_topic", "Contact request is missing topic.")
        }
        let purpose = ContactEndpointContracts.stringValue(object["purpose"])
        let requestedAction = ContactEndpointContracts.stringValue(object["requestedAction"]) ?? "contact.request.submit"
        guard endpoint.acceptedTopics.contains(topic) || endpoint.policy.allowedTopics.contains(topic) else {
            return error("topic_not_allowed", "Topic is not allowed for this endpoint.")
        }
        guard endpoint.policy.allowedActions.isEmpty || endpoint.policy.allowedActions.contains(requestedAction) else {
            return error("action_not_allowed", "Requested action is not allowed for this endpoint.")
        }
        if let purpose, endpoint.policy.allowedPurposes.isEmpty == false, endpoint.policy.allowedPurposes.contains(purpose) == false {
            return error("purpose_not_allowed", "Purpose is not allowed for this endpoint.")
        }
        if endpoint.policy.allowedDomains.isEmpty == false {
            guard let requesterDomain = requesterDomain(from: object),
                  endpoint.policy.allowedDomains.contains(requesterDomain) else {
                return error("domain_not_allowed", "Requester domain is not allowed for this endpoint.")
            }
        }
        if let requesterDomain = requesterDomain(from: object),
           endpoint.policy.blockedDomains.contains(requesterDomain) {
            return error("requester_blocked", "Requester domain is blocked for this endpoint context.")
        }
        if endpoint.policy.mode == .introductionOnly && topic != "contact.request" {
            return contractRequirement(endpoint: endpoint, reason: "introduction_only")
        }
        if endpoint.policy.mode == .contractRequired || endpoint.policy.mode == .knownRelationsOnly {
            return contractRequirement(endpoint: endpoint, reason: endpoint.policy.mode.rawValue)
        }
        guard validateRequestExpiry(object, policy: endpoint.policy, now: now) else {
            return error("request_expired_or_invalid", "Request expiresAt/issuedAt is missing, invalid, expired, or outside allowed skew.")
        }
        let payloadCharacterCount = ((try? (object["payload"] ?? .null).jsonString()) ?? "").count
        guard payloadCharacterCount <= endpoint.policy.maxPayloadCharacterCount else {
            return error("payload_too_large", "Request payload exceeds endpoint policy.")
        }
        guard endpoint.policy.allowPayloadBody || payloadIsNarrowAgreementOnly(object["payload"]) else {
            return error("payload_not_allowed", "Endpoint policy only allows agreement/introduction metadata for first contact.")
        }

        let verification = await verifyRequestSignature(object, policy: endpoint.policy)
        guard ContactEndpointContracts.boolValue(verification["verified"]) == true else {
            return [
                "status": .string("rejected"),
                "reason": .string(ContactEndpointContracts.stringValue(verification["status"]) ?? "signature_invalid"),
                "verification": .object(verification)
            ]
        }

        let requesterIdentityHash = requesterHash(from: object, fallbackRequester: requester, endpoint: endpoint)
        guard endpoint.policy.blockedRequesterHashes.contains(requesterIdentityHash) == false else {
            return error("requester_blocked", "Requester is blocked for this endpoint context.")
        }
        let nonceKey = "\(requesterIdentityHash)::\(topic)::\(nonce)"
        guard markNonceIfNew(nonceKey, now: now) else {
            return error("replay_detected", "Contact request nonce has already been seen.")
        }

        var ticket = ContactTicketRecord(
            ticketId: "ticket-\(UUID().uuidString.lowercased())",
            endpointId: endpointId,
            status: .pending,
            requestTopic: topic,
            purpose: purpose,
            requesterIdentityHash: requesterIdentityHash,
            requesterDomain: requesterDomain(from: object),
            requestPayload: sanitizedRequestPayload(object, endpoint: endpoint),
            correlationId: ContactEndpointContracts.stringValue(object["correlationId"]),
            notificationTicketId: nil,
            diagnosticMessage: nil,
            result: nil,
            createdAt: now,
            expiresAt: now.addingTimeInterval(TimeInterval(min(endpoint.ticketTTLSeconds, secondsUntil(endpoint.expiresAt, from: now) ?? endpoint.ticketTTLSeconds))),
            resolvedAt: nil,
            respondedAt: nil
        )

        // Use the proof-capable runtime owner for privileged delivery. The
        // protected owner snapshot returned by GeneralCell is intentionally
        // detached from its private vault and must not be used to authorize a
        // call into NotificationOutbox.
        let deliveryRequester = await portholeRuntimeOwner(requester: requester)
        let notificationResult = await createNotificationTicket(for: ticket, endpoint: endpoint, requester: deliveryRequester)
        ticket.notificationTicketId = ContactEndpointContracts.stringValue(notificationResult["notificationTicketId"])
        ticket.diagnosticMessage = ContactEndpointContracts.stringValue(notificationResult["diagnosticMessage"])
        if ContactEndpointContracts.stringValue(notificationResult["deliveryStatus"]) == "delivered" {
            ticket.status = .delivered
        }

        stateQueue.sync {
            ticketsByID[ticket.ticketId] = ticket
        }

        await emitEvent(
            "contact.request.received",
            payload: ticket.publicObject(includePayload: false),
            requester: requester
        )

        return ticket.publicObject(includePayload: false)
    }

    private func resolveTicket(ticketId: String, requester: Identity) async -> Object {
        let now = nowProvider()
        let mutation: TicketMutation = stateQueue.sync {
            guard var ticket = ticketsByID[ticketId] else {
                return .failure(code: "ticket_not_found_or_expired", message: "Ticket is missing or expired.")
            }
            switch ticket.status {
            case .accepted, .declined, .needsContract, .blocked:
                return .success(ticket, didTransition: false)
            case .expired, .failed:
                return .failure(code: "ticket_not_found_or_expired", message: "Ticket is missing or expired.")
            case .pending, .delivered, .resolved:
                break
            }
            guard now <= ticket.expiresAt else {
                ticket.status = .expired
                ticketsByID[ticketId] = ticket
                return .failure(code: "ticket_not_found_or_expired", message: "Ticket is missing or expired.")
            }
            switch ticket.status {
            case .pending, .delivered:
                ticket.status = .resolved
                ticket.resolvedAt = now
                ticketsByID[ticketId] = ticket
                return .success(ticket, didTransition: true)
            case .resolved:
                return .success(ticket, didTransition: false)
            case .expired, .failed, .accepted, .declined, .needsContract, .blocked:
                return .failure(code: "ticket_not_found_or_expired", message: "Ticket is missing or expired.")
            }
        }
        guard case let .success(ticket, didTransition) = mutation else {
            guard case let .failure(code, message) = mutation else {
                return error("ticket_resolution_failed", "Ticket resolution failed.")
            }
            return error(code, message)
        }
        if didTransition {
            await emitEvent("contact.ticket.resolved", payload: ticket.publicObject(includePayload: false), requester: requester)
        }
        return ticket.publicObject(includePayload: true)
    }

    private func respondTicket(ticketId: String, payload: Object, requester: Identity) async -> Object {
        let now = nowProvider()
        let requestedStatus = ContactEndpointContracts.stringValue(payload["status"])
            .flatMap(ContactTicketStatus.init(rawValue:)) ?? .accepted
        guard [.accepted, .declined, .needsContract, .blocked].contains(requestedStatus) else {
            return error("invalid_ticket_response_status", "Ticket response status must be terminal and user-selectable.")
        }
        let requestedResult = payload["result"] ?? .object([:])
        let mutation: TicketMutation = stateQueue.sync {
            guard var ticket = ticketsByID[ticketId] else {
                return .failure(code: "ticket_not_found_or_expired", message: "Ticket is missing or expired.")
            }
            if [.accepted, .declined, .needsContract, .blocked].contains(ticket.status) {
                guard ticket.status == requestedStatus,
                      Self.canonicallyEqual(ticket.result, requestedResult) else {
                    return .failure(
                        code: "ticket_already_responded",
                        message: "Ticket already has a different terminal response."
                    )
                }
                return .success(ticket, didTransition: false)
            }
            guard now <= ticket.expiresAt else {
                ticket.status = .expired
                ticketsByID[ticketId] = ticket
                return .failure(code: "ticket_not_found_or_expired", message: "Ticket is missing or expired.")
            }
            guard [.pending, .delivered, .resolved].contains(ticket.status) else {
                return .failure(
                    code: "ticket_not_respondable",
                    message: "Ticket is not in a respondable state."
                )
            }
            ticket.status = requestedStatus
            ticket.respondedAt = now
            ticket.result = requestedResult
            ticketsByID[ticketId] = ticket
            return .success(ticket, didTransition: true)
        }
        guard case let .success(ticket, didTransition) = mutation else {
            guard case let .failure(code, message) = mutation else {
                return error("ticket_response_failed", "Ticket response failed.")
            }
            return error(code, message)
        }
        if didTransition {
            await emitEvent("contact.ticket.responded", payload: ticket.publicObject(includePayload: false), requester: requester)
        }
        return ticket.publicObject(includePayload: false)
    }

    private static func canonicallyEqual(_ stored: ValueType?, _ requested: ValueType) -> Bool {
        guard let stored,
              let storedData = try? FlowCanonicalEncoder.canonicalData(
                  for: .object(["result": stored])
              ),
              let requestedData = try? FlowCanonicalEncoder.canonicalData(
                  for: .object(["result": requested])
              ) else {
            return false
        }
        return storedData == requestedData
    }

    private func upsertRoute(endpointId: String, payload: Object) -> ContactEndpointRecord? {
        stateQueue.sync {
            guard var record = endpointsByID[endpointId] else { return nil }
            var routePayload = payload
            routePayload["lastSeenAt"] = .float(nowProvider().timeIntervalSince1970)
            guard let route = ContactRouteRef(object: routePayload) else { return nil }
            if let index = record.routeRefs.firstIndex(where: { $0.id == route.id }) {
                record.routeRefs[index] = route
            } else {
                record.routeRefs.append(route)
            }
            record.updatedAt = nowProvider()
            endpointsByID[endpointId] = record
            return record
        }
    }

    private func revokeRoute(endpointId: String, routeId: String) -> ContactEndpointRecord? {
        stateQueue.sync {
            guard var record = endpointsByID[endpointId],
                  let index = record.routeRefs.firstIndex(where: { $0.id == routeId }) else {
                return nil
            }
            record.routeRefs[index].revokedAt = nowProvider()
            record.updatedAt = nowProvider()
            endpointsByID[endpointId] = record
            return record
        }
    }

    private func expireStaleRecords(now: Date? = nil) -> Object {
        let now = now ?? nowProvider()
        return stateQueue.sync {
            var expiredEndpoints = 0
            var expiredTickets = 0
            for (endpointId, var endpoint) in endpointsByID where endpoint.status == .active {
                if let expiresAt = endpoint.expiresAt, expiresAt < now {
                    endpoint.status = .expired
                    endpoint.updatedAt = now
                    endpointsByID[endpointId] = endpoint
                    expiredEndpoints += 1
                }
            }
            for (ticketId, var ticket) in ticketsByID
            where ![.accepted, .declined, .needsContract, .blocked, .expired].contains(ticket.status) {
                if ticket.expiresAt < now {
                    ticket.status = .expired
                    ticketsByID[ticketId] = ticket
                    expiredTickets += 1
                }
            }
            seenNonces = seenNonces.filter { now.timeIntervalSince($0.value) <= 7 * 24 * 60 * 60 }
            return [
                "expiredEndpoints": .integer(expiredEndpoints),
                "expiredTickets": .integer(expiredTickets),
                "seenNonceCount": .integer(seenNonces.count),
                "timestamp": .float(now.timeIntervalSince1970)
            ]
        }
    }

    private func updateEndpointStatus(endpointId: String, status: ContactEndpointStatus) -> ContactEndpointRecord? {
        stateQueue.sync {
            guard var record = endpointsByID[endpointId] else { return nil }
            record.status = status
            record.updatedAt = nowProvider()
            endpointsByID[endpointId] = record
            return record
        }
    }

    private func endpointSnapshot(endpointId: String) -> ContactEndpointRecord? {
        stateQueue.sync { endpointsByID[endpointId] }
    }

    private func markNonceIfNew(_ key: String, now: Date) -> Bool {
        stateQueue.sync {
            if seenNonces[key] != nil {
                return false
            }
            seenNonces[key] = now
            return true
        }
    }

    private func validateRequestExpiry(_ object: Object, policy: ContactEndpointPolicy, now: Date) -> Bool {
        guard let issuedAt = ContactEndpointContracts.dateValue(object["issuedAt"]) else {
            return policy.requireExpiry == false
        }
        if issuedAt.timeIntervalSince(now) > TimeInterval(policy.maxClockSkewSeconds) {
            return false
        }
        guard let expiresAt = ContactEndpointContracts.dateValue(object["expiresAt"]) else {
            return policy.requireExpiry == false
        }
        return expiresAt >= now
    }

    private func verifyRequestSignature(_ object: Object, policy: ContactEndpointPolicy) async -> Object {
        guard policy.requireSignature else {
            return ["verified": .bool(true), "status": .string("signature_not_required")]
        }
        guard case let .identity(identity)? = object["requesterIdentity"] else {
            return ["verified": .bool(false), "status": .string("missing_requester_identity")]
        }
        guard let signatureData = signatureData(from: object) else {
            return [
                "verified": .bool(false),
                "status": .string("missing_signature"),
                "signerIdentityUUID": .string(identity.uuid)
            ]
        }
        do {
            let payload = removingSignature(from: object)
            let messageData = try FlowCanonicalEncoder.canonicalData(for: .object(payload))
            let verified = await identity.verify(signature: signatureData, for: messageData)
            return [
                "verified": .bool(verified),
                "status": .string(verified ? "verified" : "invalid_signature"),
                "signerIdentityUUID": .string(identity.uuid),
                "signerDisplayName": .string(identity.displayName)
            ]
        } catch {
            return [
                "verified": .bool(false),
                "status": .string("verification_error"),
                "message": .string("\(error)"),
                "signerIdentityUUID": .string(identity.uuid)
            ]
        }
    }

    private func createNotificationTicket(
        for ticket: ContactTicketRecord,
        endpoint: ContactEndpointRecord,
        requester: Identity
    ) async -> Object {
        if let bridgeRoute = endpoint.routeRefs.first(where: { $0.isActive && $0.kind == "activeBridge" }),
           let participantId = bridgeRoute.participantId,
           let deviceId = bridgeRoute.deviceId,
           await BridgePresenceRegistry.shared.hasActiveBridge(
                participantId: participantId,
                deviceId: deviceId,
                eventType: ContactEndpointContracts.notificationTriggerEvent
           ) {
            return [
                "deliveryStatus": .string("delivered"),
                "notificationTicketId": .string("bridge-active:\(ticket.ticketId)"),
                "diagnosticMessage": .string("Active bridge route matched; push delivery skipped.")
            ]
        }

        guard let route = endpoint.routeRefs.first(where: { $0.isActive && ($0.kind == "notificationOutbox" || $0.kind == "deviceRegistration") }),
              let participantId = route.participantId else {
            return [
                "deliveryStatus": .string("queued"),
                "diagnosticMessage": .string("No active notification route with participantId; ticket remains pending inside ContactEndpoint.")
            ]
        }
        guard let outbox = try? await notificationOutboxCell(requester: requester) else {
            return [
                "deliveryStatus": .string("queued"),
                "diagnosticMessage": .string("NotificationOutbox unavailable; ticket remains pending inside ContactEndpoint.")
            ]
        }
        let response = try? await outbox.set(
            keypath: "createTicket",
            value: .object([
                "participantId": .string(participantId),
                "triggerEvent": .string(ContactEndpointContracts.notificationTriggerEvent),
                "requiredActionKey": .string(ContactEndpointContracts.requiredActionKey),
                "platform": .string(route.platform ?? "ios"),
                "ttlSeconds": .integer(Int(ticket.expiresAt.timeIntervalSince(ticket.createdAt))),
                "payload": .object([
                    "title": .string("Contact request"),
                    "message": .string("A contact endpoint has a pending request."),
                    "sourceCellEndpoint": .string(ContactEndpointContracts.endpoint),
                    "endpointId": .string(ticket.endpointId),
                    "sourceTicketId": .string(ticket.ticketId),
                    "ticketId": .string(ticket.ticketId),
                    "requestTopic": .string(ticket.requestTopic)
                ])
            ]),
            requester: requester
        )
        guard case let .object(object)? = response else {
            return [
                "deliveryStatus": .string("queued"),
                "diagnosticMessage": .string("NotificationOutbox did not return a ticket object.")
            ]
        }
        return [
            "deliveryStatus": .string("delivered"),
            "notificationTicketId": object["id"] ?? .null,
            "diagnosticMessage": object["diagnosticMessage"] ?? .null
        ]
    }

    private func persistEndpointPublicationIfRequested(record: ContactEndpointRecord, payload: Object, requester: Identity) async {
        guard ContactEndpointContracts.boolValue(payload["persistToEntityAnchor"]) == true,
              let entityAnchor = try? await entityAnchorCell(requester: requester) else {
            return
        }
        let event: Object = [
            "type": .string("contact.endpoint.published"),
            "endpointId": .string(record.endpointId),
            "cell": .string(record.cell),
            "descriptorHash": .string(record.descriptorHash),
            "at": .float(nowProvider().timeIntervalSince1970)
        ]
        _ = try? await entityAnchor.set(
            keypath: "relations.contactEndpoints.\(record.endpointId)",
            value: .object(record.publicObject()),
            requester: requester
        )
        _ = try? await entityAnchor.set(
            keypath: "chronicle[+]",
            value: .object(event),
            requester: requester
        )
    }

    private func notificationOutboxCell(requester: Identity) async throws -> NotificationOutboxCell {
        guard let resolver = CellBase.defaultCellResolver else {
            throw CellBaseError.noResolver
        }
        let cell = try await resolver.cellAtEndpoint(endpoint: "cell:///NotificationOutbox", requester: requester)
        guard let outbox = cell as? NotificationOutboxCell else {
            throw CellBaseError.noTargetMeddleCell
        }
        await outbox.ensurePortholeRuntimeBindings(requester: requester)
        return outbox
    }

    private func entityAnchorCell(requester: Identity) async throws -> Meddle? {
        guard let resolver = CellBase.defaultCellResolver else {
            throw CellBaseError.noResolver
        }
        return try await resolver.cellAtEndpoint(endpoint: "cell:///EntityAnchor", requester: requester) as? Meddle
    }

    private func emitEvent(_ title: String, payload: Object, requester: Identity) async {
        var flowElement = FlowElement(
            title: title,
            content: .object(payload),
            properties: FlowElement.Properties(type: .event, contentType: .object)
        )
        flowElement.topic = ContactEndpointContracts.flowTopic
        flowElement.origin = uuid
        pushFlowElement(flowElement, requester: requester)
    }

    private func contractRequirement(endpoint: ContactEndpointRecord, reason: String) -> Object {
        [
            "status": .string("needsContract"),
            "reason": .string(reason),
            "endpointId": .string(endpoint.endpointId),
            "requiredCapability": .string("contact.request.submit"),
            "policy": .object(endpoint.policy.publicObject())
        ]
    }

    private func error(_ code: String, _ message: String) -> Object {
        [
            "status": .string("error"),
            "code": .string(code),
            "message": .string(message)
        ]
    }

    private static func endpointId(from value: ValueType) -> String? {
        switch value {
        case .string(let endpointId):
            return endpointId.trimmingCharacters(in: .whitespacesAndNewlines).nonEmpty
        case .object(let object):
            return ContactEndpointContracts.stringValue(object["endpointId"])
        default:
            return nil
        }
    }

    private static func ticketId(from value: ValueType) -> String? {
        switch value {
        case .string(let ticketId):
            return ticketId.trimmingCharacters(in: .whitespacesAndNewlines).nonEmpty
        case .object(let object):
            return ContactEndpointContracts.stringValue(object["ticketId"])
        default:
            return nil
        }
    }

    private func requesterHash(from object: Object, fallbackRequester: Identity, endpoint: ContactEndpointRecord? = nil) -> String {
        let stableHash: String
        if case let .identity(identity)? = object["requesterIdentity"] {
            stableHash = ContactEndpointContracts.normalizedHashRef(identity.uuid)
        } else if let requesterIdentityRef = ContactEndpointContracts.stringValue(object["requesterIdentityRef"]) {
            stableHash = ContactEndpointContracts.normalizedHashRef(requesterIdentityRef)
        } else {
            stableHash = ContactEndpointContracts.normalizedHashRef(fallbackRequester.uuid)
        }
        guard let endpoint else {
            return stableHash
        }
        return ContactEndpointContracts.normalizedHashRef([
            "contact-requester-context-v1",
            endpoint.endpointId,
            endpoint.cell,
            stableHash
        ].joined(separator: "::"))
    }

    private func requesterDomain(from object: Object) -> String? {
        ContactEndpointContracts.stringValue(object["requesterDomain"])
            ?? ContactEndpointContracts.stringValue(object["requesterIdentityDomain"])
    }

    private func sanitizedRequestPayload(_ object: Object, endpoint: ContactEndpointRecord) -> Object {
        var sanitized = object
        sanitized.removeValue(forKey: "signature")
        sanitized.removeValue(forKey: "signatureBase64")
        if case let .identity(identity)? = sanitized["requesterIdentity"] {
            sanitized["requesterIdentity"] = .object([
                "contextHash": .string(requesterHash(from: object, fallbackRequester: identity, endpoint: endpoint)),
                "displayName": .string(identity.displayName)
            ])
        }
        return sanitized
    }

    private func requiredProofRoles(for object: Object, record: ContactEndpointRecord) -> Set<ContactProofRole> {
        var roles = Set(ContactEndpointContracts.stringList(object["requiredProofRoles"]).compactMap(ContactProofRole.init(rawValue:)))
        roles.insert(.endpointOwner)
        if record.custodyMode != "userControlledVault" {
            roles.insert(.custodian)
        }
        return roles
    }

    private func validateCustodyPayload(_ object: Object) -> Object? {
        let custodyMode = ContactEndpointContracts.stringValue(object["custodyMode"]) ?? "userControlledVault"
        guard custodyMode != "userControlledVault" else { return nil }
        guard let custodian = ContactEndpointContracts.objectValue(object["custodianRef"] ?? object["custodian"]) else {
            return error("missing_custodian", "Temporary custody requires a custodianRef object.")
        }
        let forbiddenKeys = ["privateKey", "secretKey", "seed", "mnemonic", "vaultExport", "rawPrivateKey"]
        if forbiddenKeys.contains(where: { custodian[$0] != nil }) {
            return error("custodian_private_key_material", "Custodian payload must never contain private key material.")
        }
        guard ContactEndpointContracts.stringValue(custodian["custodianIdentityRef"]) != nil
                || ContactEndpointContracts.objectValue(custodian["custodianIdentity"]) != nil
                || ContactEndpointContracts.stringValue(custodian["publicKeyRef"]) != nil else {
            return error("missing_custodian_identity", "Temporary custody requires a new custodian identity/public key reference.")
        }
        guard ContactEndpointContracts.dateValue(custodian["expiresAt"]) != nil else {
            return error("missing_custodian_expiry", "Temporary custody requires an expiresAt value.")
        }
        return nil
    }

    private func sanitizedCustodianRef(from object: Object) -> Object? {
        guard var custodian = ContactEndpointContracts.objectValue(object["custodianRef"] ?? object["custodian"]) else {
            return nil
        }
        for key in ["privateKey", "secretKey", "seed", "mnemonic", "vaultExport", "rawPrivateKey"] {
            custodian.removeValue(forKey: key)
        }
        return custodian
    }

    private func isSupportedEndpointCellAddress(_ address: String) -> Bool {
        let normalized = address.trimmingCharacters(in: .whitespacesAndNewlines)
        if normalized == ContactEndpointContracts.endpoint {
            return true
        }
        guard normalized.hasPrefix("cell://") else {
            return false
        }
        guard let url = URL(string: normalized) else {
            return false
        }
        return url.path == "/ContactEndpoint" || url.path == "ContactEndpoint"
    }

    private func payloadIsNarrowAgreementOnly(_ value: ValueType?) -> Bool {
        guard let value else { return true }
        switch value {
        case .null:
            return true
        case .object(let object):
            guard object.isEmpty == false else { return true }
            let allowedKeys = Set(["agreementProposal", "introductionRef", "capabilitiesRequested", "purpose", "messageRef"])
            return Set(object.keys).isSubset(of: allowedKeys)
        default:
            return false
        }
    }

    private func deviceRouteAllowsCallback(payload: Object) -> Bool {
        guard let endpointId = ContactEndpointContracts.stringValue(payload["endpointId"]),
              let participantId = ContactEndpointContracts.stringValue(payload["participantId"]),
              let deviceId = ContactEndpointContracts.stringValue(payload["deviceId"]),
              let endpoint = endpointSnapshot(endpointId: endpointId) else {
            return false
        }
        return endpoint.routeRefs.contains { route in
            route.isActive
                && route.participantId == participantId
                && route.deviceId == deviceId
                && (route.kind == "activeBridge" || route.kind == "deviceRegistration" || route.kind == "notificationOutbox")
        }
    }

    private func signatureData(from object: Object) -> Data? {
        if case let .data(data)? = object["signature"] {
            return data
        }
        if let encoded = ContactEndpointContracts.stringValue(object["signatureBase64"]) {
            return Data(base64Encoded: encoded)
        }
        return nil
    }

    private func removingSignature(from object: Object) -> Object {
        var payload = object
        payload.removeValue(forKey: "signature")
        payload.removeValue(forKey: "signatureBase64")
        return payload
    }

    private func secondsUntil(_ date: Date?, from now: Date) -> Int? {
        guard let date else { return nil }
        return max(0, Int(date.timeIntervalSince(now)))
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
