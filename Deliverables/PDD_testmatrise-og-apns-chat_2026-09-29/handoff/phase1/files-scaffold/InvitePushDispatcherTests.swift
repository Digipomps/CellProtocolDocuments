// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

@testable import App
import Foundation
import XCTest
@preconcurrency import CellBase

/// WP2/WP3 on the scaffold side — T5.1 (token belongs to an entity) and T5.3 (only who was invited is pushed).
final class InvitePushDispatcherTests: XCTestCase {

    private let token = String(repeating: "ab12cd34", count: 8)
    private let bundle = "org.digipomps.haven"

    // MARK: fixtures

    private struct Entity {
        let vault: EphemeralIdentityVault
        let identity: Identity
    }

    private func entity(_ name: String) async -> Entity {
        let vault = EphemeralIdentityVault()
        var identity = Identity(UUID().uuidString, displayName: name, identityVault: nil)
        await vault.addIdentity(identity: &identity, for: "private")
        return Entity(vault: vault, identity: identity)
    }

    private func publication(issuer: Entity, audienceEntity: String?) async throws -> HavenInvitePublication {
        let descriptor = try XCTUnwrap(IdentityPublicKeySignatureVerifier.descriptor(for: issuer.identity))
        let createdAt = Int(Date().timeIntervalSince1970)
        var ticket = HavenInviteTicket(
            ticketID: "inv-" + UUID().uuidString.lowercased(),
            issuer: descriptor, issuerDisplayName: "Kjetil", issuerContactEndpoint: "ep-1",
            audienceToken: "aud-vegar", audienceKind: "email", humanCode: "ABC234",
            greetingName: "Vegar", identityDomain: "private", basis: [],
            createdAt: createdAt, expiresAt: createdAt + HavenInviteTicket.defaultTimeToLive,
            nonce: Data(repeating: 7, count: 12)
        )
        ticket.proof = try await HavenInviteSigning.proof(over: try ticket.canonicalPayloadData(), by: issuer.identity)
        var publication = HavenInvitePublication(
            ticketID: ticket.ticketID, humanCode: ticket.humanCode,
            ticketToken: try HavenInviteLink.encode(ticket), audienceToken: ticket.audienceToken,
            issuerIdentityUUID: ticket.issuer.uuid, expiresAt: ticket.expiresAt, publishedAt: createdAt,
            statusKey: HavenInvitePublication.makeStatusKey(), audienceEntity: audienceEntity
        )
        publication.proof = try await HavenInviteSigning.proof(over: try publication.canonicalPayloadData(), by: issuer.identity)
        return publication
    }

    private func register(_ service: PushRegistryService, _ who: Entity, token: String? = nil) async throws -> String {
        let registration = try await HavenPushRegistration.make(
            entity: who.identity, environment: .sandbox, bundleId: bundle, token: token ?? self.token
        )
        return try await service.register(registration)
    }

    // MARK: T5.1 — registry on the scaffold

    func testRegisterPersistsAndSurvivesARestart() async throws {
        let dir = FileManager.default.temporaryDirectory.appendingPathComponent("push-registry-\(UUID().uuidString)")
        defer { try? FileManager.default.removeItem(at: dir) }
        let store = FilePushRegistryStore(url: dir.appendingPathComponent("registry.json"))
        let vegar = await entity("vegar")

        let first = try PushRegistryService(store: store)
        let registrationID = try await register(first, vegar)

        let restarted = try PushRegistryService(store: store)
        let snapshot = await restarted.snapshot()
        XCTAssertEqual(snapshot.activeRegistrations(entity: vegar.identity.uuid).map(\.registrationID), [registrationID])

        let attributes = try FileManager.default.attributesOfItem(atPath: store.url.path)
        XCTAssertEqual((attributes[.posixPermissions] as? NSNumber)?.intValue, 0o600)
    }

    func testStoredFileHoldsNoNameAndNoTokenAfterRevocation() async throws {
        let dir = FileManager.default.temporaryDirectory.appendingPathComponent("push-registry-\(UUID().uuidString)")
        defer { try? FileManager.default.removeItem(at: dir) }
        let store = FilePushRegistryStore(url: dir.appendingPathComponent("registry.json"))
        let vegar = await entity("vegar-navn")
        let service = try PushRegistryService(store: store)
        let registrationID = try await register(service, vegar)
        try await service.revoke(try await HavenPushRevocation.make(registrationID: registrationID, by: vegar.identity))

        let text = String(decoding: try Data(contentsOf: store.url), as: UTF8.self)
        XCTAssertFalse(text.contains(token), "a revoked token must be gone from disk")
        XCTAssertFalse(text.contains("vegar-navn"), "no display name is stored")
    }

    func testUnsignedRegistrationIsNotStored() async throws {
        let vegar = await entity("vegar")
        let service = try PushRegistryService()
        var registration = try await HavenPushRegistration.make(entity: vegar.identity, environment: .sandbox, bundleId: bundle, token: token)
        registration.proof = nil
        do { _ = try await service.register(registration); XCTFail("must be refused") }
        catch { XCTAssertEqual(error as? HavenPushVerifier.Failure, .unsigned) }
        let snapshot = await service.snapshot()
        XCTAssertTrue(snapshot.records.isEmpty)
    }

    // MARK: T5.3 — dispatch

    func testDispatchSendsExactlyOnePushToTheNamedAndRegisteredEntity() async throws {
        let kjetil = await entity("kjetil"), vegar = await entity("vegar"), stranger = await entity("stranger")
        let service = try PushRegistryService()
        let registrationID = try await register(service, vegar)
        _ = try await register(service, stranger, token: String(repeating: "ef56ab78", count: 8))
        let sender = RecordingSender()
        let dispatcher = InvitePushDispatcher(registry: service, sender: sender)

        let pub = try await publication(issuer: kjetil, audienceEntity: vegar.identity.uuid)
        let log = await dispatcher.dispatch(publication: pub)

        XCTAssertEqual(log.map(\.outcome), [.sent])
        XCTAssertEqual(log.first?.registrationID, registrationID)
        let sent = await sender.sent()
        XCTAssertEqual(sent.count, 1)
        XCTAssertEqual(sent.first?.token, token)
        XCTAssertEqual(sent.first?.ticketID, pub.ticketID)
        let body = String(decoding: try XCTUnwrap(sent.first).payloadData(), as: UTF8.self)
        XCTAssertFalse(body.contains("Kjetil"), "the push never names the sender")
    }

    func testNothingIsSentWithoutANamedAudienceEntity() async throws {
        let kjetil = await entity("kjetil"), vegar = await entity("vegar")
        let service = try PushRegistryService()
        _ = try await register(service, vegar)
        let sender = RecordingSender()
        let dispatcher = InvitePushDispatcher(registry: service, sender: sender)

        let log = await dispatcher.dispatch(publication: try await publication(issuer: kjetil, audienceEntity: nil))
        XCTAssertEqual(log.map(\.outcome), [.noAudienceEntity])
        let sent = await sender.sent()
        XCTAssertTrue(sent.isEmpty, "a registered stranger must not get the push just because the token exists")
    }

    func testNamedButUnregisteredAudienceIsLoggedNotSent() async throws {
        let kjetil = await entity("kjetil"), vegar = await entity("vegar")
        let sender = RecordingSender()
        let dispatcher = InvitePushDispatcher(registry: try PushRegistryService(), sender: sender)
        let log = await dispatcher.dispatch(publication: try await publication(issuer: kjetil, audienceEntity: vegar.identity.uuid))
        XCTAssertEqual(log.map(\.outcome), [.noRegistration])
        let sent = await sender.sent()
        XCTAssertTrue(sent.isEmpty)
    }

    func testRevokedAndTombstonedAreNotSent() async throws {
        let kjetil = await entity("kjetil"), vegar = await entity("vegar")
        let service = try PushRegistryService()
        _ = try await register(service, vegar)
        let pub = try await publication(issuer: kjetil, audienceEntity: vegar.identity.uuid)
        let sender = RecordingSender()

        let revoked = InvitePushDispatcher(registry: service, sender: sender, revokedTicketIDs: { [pub.ticketID] })
        let revokedLog = await revoked.dispatch(publication: pub)
        XCTAssertEqual(revokedLog.map(\.outcome), [.ticketRevoked])

        let ticket = try HavenInviteLink.decode(pub.ticketToken)
        let reply = try await HavenInviteReply.make(to: ticket, decision: .never, by: vegar.identity)
        var ledger = HavenInviteTombstoneLedger()
        ledger.record(try HavenInviteTombstone.make(from: reply, forTicket: ticket))
        let closed = InvitePushDispatcher(registry: service, sender: sender, tombstones: { ledger })
        let closedLog = await closed.dispatch(publication: pub)
        XCTAssertEqual(closedLog.map(\.outcome), [.tombstoned])

        let sent = await sender.sent()
        XCTAssertTrue(sent.isEmpty)
    }

    func testApnsUnregisteredRevokesTheTokenAndNextDispatchSaysTokenRevoked() async throws {
        let kjetil = await entity("kjetil"), vegar = await entity("vegar")
        let service = try PushRegistryService()
        _ = try await register(service, vegar)
        let sender = RecordingSender(result: PushSendResult(providerMessageID: nil, accepted: false, diagnosticMessage: "APNS rejected push: Unregistered"))
        let dispatcher = InvitePushDispatcher(registry: service, sender: sender)

        let first = await dispatcher.dispatch(publication: try await publication(issuer: kjetil, audienceEntity: vegar.identity.uuid))
        XCTAssertEqual(first.map(\.outcome), [.tokenRevoked])
        let second = await dispatcher.dispatch(publication: try await publication(issuer: kjetil, audienceEntity: vegar.identity.uuid))
        XCTAssertEqual(second.map(\.outcome), [.tokenRevoked])
        let sent = await sender.sent()
        XCTAssertEqual(sent.count, 1, "no second attempt on a token APNs said is dead")
    }

    func testOtherApnsRefusalIsTransportRefusedAndKeepsTheToken() async throws {
        let kjetil = await entity("kjetil"), vegar = await entity("vegar")
        let service = try PushRegistryService()
        _ = try await register(service, vegar)
        let sender = RecordingSender(result: PushSendResult(providerMessageID: nil, accepted: false, diagnosticMessage: "APNS rejected push: TooManyRequests"))
        let dispatcher = InvitePushDispatcher(registry: service, sender: sender)
        let log = await dispatcher.dispatch(publication: try await publication(issuer: kjetil, audienceEntity: vegar.identity.uuid))
        XCTAssertEqual(log.map(\.outcome), [.transportRefused])
        let snapshot = await service.snapshot()
        XCTAssertEqual(snapshot.activeRegistrations(entity: vegar.identity.uuid).count, 1)
    }

    func testWithoutApnsConfigurationItDecidesAndLogsTransportRefused() async throws {
        let kjetil = await entity("kjetil"), vegar = await entity("vegar")
        let service = try PushRegistryService()
        _ = try await register(service, vegar)
        let dispatcher = InvitePushDispatcher(registry: service, sender: nil)
        let log = await dispatcher.dispatch(publication: try await publication(issuer: kjetil, audienceEntity: vegar.identity.uuid))
        XCTAssertEqual(log.map(\.outcome), [.transportRefused])
        XCTAssertEqual(log.first?.detail, "apns_not_configured")
    }

    func testLogNeverHoldsTheToken() async throws {
        let kjetil = await entity("kjetil"), vegar = await entity("vegar")
        let service = try PushRegistryService()
        _ = try await register(service, vegar)
        let dispatcher = InvitePushDispatcher(registry: service, sender: RecordingSender())
        _ = await dispatcher.dispatch(publication: try await publication(issuer: kjetil, audienceEntity: vegar.identity.uuid))
        let entries = await dispatcher.entries
        for entry in entries {
            XCTAssertFalse("\(entry)".contains(token), "the log holds registration IDs, never tokens")
        }
    }
}

private actor RecordingSender: InviteApnsSending {
    private var pushes: [InviteApnsPush] = []
    private let result: PushSendResult
    init(result: PushSendResult = PushSendResult(providerMessageID: "apns-1", accepted: true, diagnosticMessage: nil)) {
        self.result = result
    }
    func sendInvite(_ push: InviteApnsPush) async throws -> PushSendResult {
        pushes.append(push)
        return result
    }
    func sent() -> [InviteApnsPush] { pushes }
}
