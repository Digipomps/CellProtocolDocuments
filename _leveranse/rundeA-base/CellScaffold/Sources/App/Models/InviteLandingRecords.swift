// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

//
//  InviteLandingRecords.swift
//  CellScaffold
//
//  What the scaffold stores about an invitation, and nothing more.
//
//  The scaffold is a relay and a counter. It holds the ticket someone already
//  published, counts how many times the landing page served it, keeps replies
//  until the issuer collects them, and remembers what has been withdrawn. It
//  never learns who the invitation was addressed to — only the truncated
//  audience token the issuer chose to include — and it holds no key that could
//  mint or alter one.
//

import Crypto
import Fluent
import Vapor
@preconcurrency import CellBase

/// A published ticket. Row lifetime is the ticket's own lifetime plus a grace
/// period; nothing here is worth keeping after that.
final class InviteTicketRecord: Model, Content, @unchecked Sendable {
    static let schema = "invite_tickets"

    @ID
    var id: UUID?

    /// The issuer's ticket id. Unique, and the join key for replies.
    @Field(key: "ticket_id")
    var ticketID: String

    /// Six characters, the short-link lookup key. Unique, so a collision is a
    /// hard failure at publish time rather than a silent mix-up later.
    @Field(key: "human_code")
    var humanCode: String

    /// The self-contained ticket, exactly as published. Served back verbatim.
    @Field(key: "ticket_token")
    var ticketToken: String

    @Field(key: "audience_token")
    var audienceToken: String

    @Field(key: "issuer_identity_uuid")
    var issuerIdentityUUID: String

    @Field(key: "issuer_display_name")
    var issuerDisplayName: String

    /// SHA-256 digest of the high-entropy bearer token for the issuer's own
    /// status and inbox reads. The bearer token itself is never persisted.
    @Field(key: "status_key")
    var statusKeyDigest: String

    @Field(key: "expires_at")
    var expiresAt: Date

    @Field(key: "max_contact_requests")
    var maxContactRequests: Int

    @Field(key: "open_count")
    var openCount: Int

    @OptionalField(key: "first_opened_at")
    var firstOpenedAt: Date?

    @OptionalField(key: "responded_at")
    var respondedAt: Date?

    @OptionalField(key: "resulting_entity_ref")
    var resultingEntityRef: String?

    @OptionalField(key: "revoked_at")
    var revokedAt: Date?

    @OptionalField(key: "revocation_reason")
    var revocationReason: String?

    @Timestamp(key: "created_at", on: .create)
    var createdAt: Date?

    init() {}

    init(
        id: UUID? = nil,
        ticketID: String,
        humanCode: String,
        ticketToken: String,
        audienceToken: String,
        issuerIdentityUUID: String,
        issuerDisplayName: String,
        statusKey: String,
        expiresAt: Date,
        maxContactRequests: Int
    ) {
        self.id = id
        self.ticketID = ticketID
        self.humanCode = humanCode
        self.ticketToken = ticketToken
        self.audienceToken = audienceToken
        self.issuerIdentityUUID = issuerIdentityUUID
        self.issuerDisplayName = issuerDisplayName
        self.statusKeyDigest = Self.digestStatusKey(statusKey)
        self.expiresAt = expiresAt
        self.maxContactRequests = maxContactRequests
        self.openCount = 0
    }

    var isRevoked: Bool { revokedAt != nil }

    func isExpired(now: Date = Date()) -> Bool { now > expiresAt }

    /// Constant-time-ish comparison. A length check first is fine — the key is
    /// fixed length, so length never varies with the secret.
    func matchesStatusKey(_ candidate: String) -> Bool {
        let candidateDigest = Self.digestStatusKey(candidate)
        guard candidateDigest.utf8.count == statusKeyDigest.utf8.count else { return false }
        var difference: UInt8 = 0
        for (left, right) in zip(candidateDigest.utf8, statusKeyDigest.utf8) {
            difference |= left ^ right
        }
        return difference == 0
    }

    static func digestStatusKey(_ key: String) -> String {
        SHA256.hash(data: Data(key.utf8))
            .map { String(format: "%02x", $0) }
            .joined()
    }

    func lifecycle(now: Date = Date()) -> HavenInviteLifecycle {
        if isRevoked { return .revoked }
        if respondedAt != nil { return resultingEntityRef == nil ? .declined : .accepted }
        if isExpired(now: now) { return .expired }
        if openCount > 0 { return .opened }
        return .published
    }
}

/// Enforces the invitation relay's bounded retention contract.
///
/// - Collected contact requests are deleted in the same database transaction
///   that claims them for delivery.
/// - Expired tickets and any uncollected replies are deleted after one day of
///   grace, both at process startup and by the scheduled production sweep.
enum InviteLandingRetention {
    static let expiredTicketGracePeriod: TimeInterval = 24 * 60 * 60

    struct PurgeReceipt: Equatable, Sendable {
        var ticketsDeleted: Int
        var contactRequestsDeleted: Int
    }

    /// Upgrades rows written before status bearers were stored as digests.
    /// V1 raw bearers are 32-byte base64url strings; digests are lowercase
    /// SHA-256 hex, so the persisted formats are unambiguous.
    static func digestLegacyStatusKeys(on database: any Database) async throws -> Int {
        try await database.transaction { transaction in
            let records = try await InviteTicketRecord.query(on: transaction).all()
            let legacyRecords = records.filter { record in
                let value = record.statusKeyDigest
                return value.count != 64 || value.contains { !$0.isHexDigit || $0.isUppercase }
            }
            for record in legacyRecords {
                record.statusKeyDigest = InviteTicketRecord.digestStatusKey(record.statusKeyDigest)
                try await record.save(on: transaction)
            }
            return legacyRecords.count
        }
    }

    static func collectUncollectedPayloads(
        ticketID: String,
        on database: any Database
    ) async throws -> [String] {
        try await database.transaction { transaction in
            let rows = try await InviteContactRequestRecord.query(on: transaction)
                .filter(\.$ticketID == ticketID)
                .filter(\.$collectedAt == nil)
                .all()
            let payloads = rows.map(\.payloadJSON)
            try await rows.delete(on: transaction)
            return payloads
        }
    }

    static func purgeExpired(
        on database: any Database,
        now: Date = Date()
    ) async throws -> PurgeReceipt {
        let cutoff = now.addingTimeInterval(-expiredTicketGracePeriod)
        return try await database.transaction { transaction in
            let previouslyCollected = try await InviteContactRequestRecord.query(on: transaction)
                .filter(\.$collectedAt != nil)
                .all()
            try await previouslyCollected.delete(on: transaction)

            let tickets = try await InviteTicketRecord.query(on: transaction)
                .filter(\.$expiresAt <= cutoff)
                .all()
            var contactRequestCount = previouslyCollected.count
            for ticket in tickets {
                let rows = try await InviteContactRequestRecord.query(on: transaction)
                    .filter(\.$ticketID == ticket.ticketID)
                    .all()
                contactRequestCount += rows.count
                try await rows.delete(on: transaction)
            }
            try await tickets.delete(on: transaction)
            return PurgeReceipt(
                ticketsDeleted: tickets.count,
                contactRequestsDeleted: contactRequestCount
            )
        }
    }
}

/// A reply, held only until the issuer collects it.
final class InviteContactRequestRecord: Model, Content, @unchecked Sendable {
    static let schema = "invite_contact_requests"

    @ID
    var id: UUID?

    @Field(key: "request_id")
    var requestID: String

    @Field(key: "ticket_id")
    var ticketID: String

    /// The signed envelope, verbatim. The scaffold verified it once on the way
    /// in; the issuer verifies it again on the way out, against the key it
    /// carries. Storing the original is what makes the second check possible.
    @Field(key: "payload_json")
    var payloadJSON: String

    @Field(key: "sender_display_name")
    var senderDisplayName: String

    @OptionalField(key: "collected_at")
    var collectedAt: Date?

    @Timestamp(key: "created_at", on: .create)
    var createdAt: Date?

    init() {}

    init(
        id: UUID? = nil,
        requestID: String,
        ticketID: String,
        payloadJSON: String,
        senderDisplayName: String
    ) {
        self.id = id
        self.requestID = requestID
        self.ticketID = ticketID
        self.payloadJSON = payloadJSON
        self.senderDisplayName = senderDisplayName
    }
}

// MARK: - Migration

struct CreateInviteLandingTables: AsyncMigration {
    func prepare(on database: Database) async throws {
        try await database.schema(InviteTicketRecord.schema)
            .id()
            .field("ticket_id", .string, .required)
            .field("human_code", .string, .required)
            .field("ticket_token", .string, .required)
            .field("audience_token", .string, .required)
            .field("issuer_identity_uuid", .string, .required)
            .field("issuer_display_name", .string, .required)
            .field("status_key", .string, .required)
            .field("expires_at", .datetime, .required)
            .field("max_contact_requests", .int, .required)
            .field("open_count", .int, .required)
            .field("first_opened_at", .datetime)
            .field("responded_at", .datetime)
            .field("resulting_entity_ref", .string)
            .field("revoked_at", .datetime)
            .field("revocation_reason", .string)
            .field("created_at", .datetime)
            .unique(on: "ticket_id")
            .unique(on: "human_code")
            .create()

        try await database.schema(InviteContactRequestRecord.schema)
            .id()
            .field("request_id", .string, .required)
            .field("ticket_id", .string, .required)
            .field("payload_json", .string, .required)
            .field("sender_display_name", .string, .required)
            .field("collected_at", .datetime)
            .field("created_at", .datetime)
            .unique(on: "request_id")
            .create()
    }

    func revert(on database: Database) async throws {
        try await database.schema(InviteContactRequestRecord.schema).delete()
        try await database.schema(InviteTicketRecord.schema).delete()
    }
}
