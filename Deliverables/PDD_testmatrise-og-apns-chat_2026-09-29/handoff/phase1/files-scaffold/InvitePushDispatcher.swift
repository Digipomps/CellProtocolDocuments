// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

//
//  InvitePushDispatcher.swift
//  CellScaffold
//
//  Token registry (push.register / push.revoke) and the dispatcher that pushes a
//  published invitation (invite.push) — contract apns_invite_v1.
//
//  The decision lives in CellProtocol (HavenInvitePushPlanner); this file only
//  carries it out: build the payload, send it, and write what happened to the
//  scaffold's own log. The outcome is never returned to the invitation's sender
//  (purpose://candidate.testmatrise.apns.only-who-was-invited-is-pushed).
//

import Foundation
@preconcurrency import CellBase

// MARK: - Sending

protocol InviteApnsSending: Sendable {
    func sendInvite(_ push: InviteApnsPush) async throws -> PushSendResult
}

extension APNSPushProviderAdapter: InviteApnsSending {}

// MARK: - Registry persistence

protocol PushRegistryStoring: Sendable {
    func load() throws -> HavenPushRegistry?
    func save(_ registry: HavenPushRegistry) throws
}

/// One JSON file, written atomically with mode 0600. Holds only what HavenPushRegistry holds.
struct FilePushRegistryStore: PushRegistryStoring {
    let url: URL

    func load() throws -> HavenPushRegistry? {
        guard FileManager.default.fileExists(atPath: url.path) else { return nil }
        return try JSONDecoder().decode(HavenPushRegistry.self, from: try Data(contentsOf: url))
    }

    func save(_ registry: HavenPushRegistry) throws {
        let data = try JSONEncoder().encode(registry)
        try FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        try data.write(to: url, options: [.atomic])
        try FileManager.default.setAttributes([.posixPermissions: 0o600], ofItemAtPath: url.path)
    }
}

actor PushRegistryService {
    private var registry: HavenPushRegistry
    private let store: (any PushRegistryStoring)?

    init(store: (any PushRegistryStoring)? = nil) throws {
        self.store = store
        self.registry = try store?.load() ?? HavenPushRegistry()
    }

    /// Verifies, stores, persists. Returns the registration ID the app keeps for later revocation.
    func register(_ registration: HavenPushRegistration, now: Date = Date()) throws -> String {
        var next = registry
        let record = try next.register(registration, now: now)
        try store?.save(next)
        registry = next
        return record.registrationID
    }

    func revoke(_ revocation: HavenPushRevocation, now: Date = Date()) throws {
        var next = registry
        try next.revoke(revocation, now: now)
        try store?.save(next)
        registry = next
    }

    func markUnregistered(registrationID: String, now: Date = Date()) {
        var next = registry
        next.markUnregistered(registrationID: registrationID, now: now)
        registry = next                    // the token is dead whether or not the file write succeeds
        try? store?.save(next)
    }

    func snapshot() -> HavenPushRegistry { registry }
}

// MARK: - Dispatch

/// The scaffold's internal record of one push decision. Holds the registration ID, never the token.
struct InvitePushLogEntry: Equatable, Sendable {
    var ticketID: String
    var registrationID: String?
    var outcome: HavenInvitePushOutcome
    var at: Int
    var detail: String?
}

actor InvitePushDispatcher {

    private let registry: PushRegistryService
    private let sender: (any InviteApnsSending)?
    private let revokedTicketIDs: @Sendable () async -> Set<String>
    private let tombstones: @Sendable () async -> HavenInviteTombstoneLedger
    private let clock: @Sendable () -> Date
    private(set) var entries: [InvitePushLogEntry] = []
    private static let maxEntries = 500

    /// `sender == nil` is the scaffold without APNS credentials: it still decides, and logs `transport_refused`.
    init(
        registry: PushRegistryService,
        sender: (any InviteApnsSending)?,
        revokedTicketIDs: @escaping @Sendable () async -> Set<String> = { [] },
        tombstones: @escaping @Sendable () async -> HavenInviteTombstoneLedger = { HavenInviteTombstoneLedger() },
        clock: @escaping @Sendable () -> Date = { Date() }
    ) {
        self.registry = registry
        self.sender = sender
        self.revokedTicketIDs = revokedTicketIDs
        self.tombstones = tombstones
        self.clock = clock
    }

    /// Never throws, and returns nothing that belongs in a response to the sender; the result is for tests and logs.
    @discardableResult
    func dispatch(publication: HavenInvitePublication) async -> [InvitePushLogEntry] {
        let now = clock()
        let plan = HavenInvitePushPlanner.plan(
            publication: publication,
            revokedTicketIDs: await revokedTicketIDs(),
            tombstones: await tombstones(),
            registry: await registry.snapshot(),
            now: now
        )
        if let skip = plan.skip {
            return record([entry(plan.ticketID, nil, skip, now)])
        }
        var written: [InvitePushLogEntry] = []
        for target in plan.targets {
            written.append(await send(to: target, plan: plan, now: now))
        }
        return record(written)
    }

    private func send(to target: HavenInvitePushTarget, plan: HavenInvitePushPlan, now: Date) async -> InvitePushLogEntry {
        let environment: InviteApnsEnvironment = target.environment == .sandbox ? .sandbox : .production
        let push: InviteApnsPush
        do {
            push = try InviteApnsPush.make(
                ticketID: plan.ticketID, environment: environment, bundleID: target.bundleId,
                token: target.token, ticketExpiresAt: plan.ticketExpiresAt, now: now
            )
        } catch {
            return entry(plan.ticketID, target.registrationID, .transportRefused, now, "payload_not_built:\(error)")
        }
        guard let sender else {
            return entry(plan.ticketID, target.registrationID, .transportRefused, now, "apns_not_configured")
        }
        do {
            let result = try await sender.sendInvite(push)
            if result.accepted { return entry(plan.ticketID, target.registrationID, .sent, now) }
            let diagnostic = result.diagnosticMessage ?? ""
            if Self.meansTokenIsDead(diagnostic) {
                await registry.markUnregistered(registrationID: target.registrationID, now: now)
                return entry(plan.ticketID, target.registrationID, .tokenRevoked, now, diagnostic)
            }
            return entry(plan.ticketID, target.registrationID, .transportRefused, now, diagnostic)
        } catch {
            return entry(plan.ticketID, target.registrationID, .transportRefused, now, "transport_error:\(error)")
        }
    }

    /// APNs reasons that mean "this token will never work again".
    private static func meansTokenIsDead(_ diagnostic: String) -> Bool {
        ["Unregistered", "BadDeviceToken", "DeviceTokenNotForTopic", "ExpiredToken"].contains { diagnostic.contains($0) }
    }

    private func entry(_ ticketID: String, _ registrationID: String?, _ outcome: HavenInvitePushOutcome, _ now: Date, _ detail: String? = nil) -> InvitePushLogEntry {
        InvitePushLogEntry(ticketID: ticketID, registrationID: registrationID, outcome: outcome, at: Int(now.timeIntervalSince1970), detail: detail)
    }

    private func record(_ new: [InvitePushLogEntry]) -> [InvitePushLogEntry] {
        entries.append(contentsOf: new)
        if entries.count > Self.maxEntries { entries.removeFirst(entries.count - Self.maxEntries) }
        return new
    }
}
