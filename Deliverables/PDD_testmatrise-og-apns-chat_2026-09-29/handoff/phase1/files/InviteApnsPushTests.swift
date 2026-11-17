// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

@testable import App
import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking
#endif
import XCTest

/// WP1 / T5.2 — payload carries no content (contract apns_invite_v1).
/// purpose://candidate.testmatrise.apns.payload-carries-no-content
final class InviteApnsPushTests: XCTestCase {

    private static let ticketID = "inv-0a1b2c3d-4e5f-6071-8293-a4b5c6d7e8f9"
    private static let token = String(repeating: "ab12cd34", count: 8)   // 64 hex
    private static let now = Date(timeIntervalSince1970: 1_800_000_000)

    /// Golden bytes. A change here is a contract change (bump apns_invite_v1.version).
    private static let golden =
        #"{"aps":{"alert":{"body":"Du har en invitasjon å svare på.","title":"HAVEN"}},"haven":{"id":"inv-0a1b2c3d-4e5f-6071-8293-a4b5c6d7e8f9","k":"invite"}}"#

    private func make(
        ticketID: String = ticketID,
        environment: InviteApnsEnvironment = .sandbox,
        bundleID: String = "org.digipomps.haven",
        token: String = token,
        ticketExpiresAt: Int = 1_800_000_000 + 30 * 86_400
    ) throws -> InviteApnsPush {
        try InviteApnsPush.make(
            ticketID: ticketID, environment: environment, bundleID: bundleID,
            token: token, ticketExpiresAt: ticketExpiresAt, now: Self.now
        )
    }

    func testPayloadMatchesGoldenBytes() throws {
        let data = try make().payloadData()
        XCTAssertEqual(String(decoding: data, as: UTF8.self), Self.golden)
        XCTAssertLessThanOrEqual(data.count, InviteApnsPush.maxPayloadBytes)
    }

    func testPayloadCarriesOnlyTheAgreedKeys() throws {
        let object = try XCTUnwrap(JSONSerialization.jsonObject(with: try make().payloadData()) as? [String: Any])
        XCTAssertEqual(Set(object.keys), ["aps", "haven"])
        let aps = try XCTUnwrap(object["aps"] as? [String: Any])
        XCTAssertEqual(Set(aps.keys), ["alert"], "no sound, badge, thread-id or content-available in v1")
        let alert = try XCTUnwrap(aps["alert"] as? [String: Any])
        XCTAssertEqual(Set(alert.keys), ["title", "body"])
        let haven = try XCTUnwrap(object["haven"] as? [String: Any])
        XCTAssertEqual(Set(haven.keys), ["k", "id"])
        XCTAssertEqual(haven["k"] as? String, "invite")
        XCTAssertEqual(haven["id"] as? String, Self.ticketID)
    }

    func testPayloadNeverNamesTheSenderOrCarriesText() throws {
        // The builder takes no sender, name or message argument at all; this pins that
        // nothing but fixed text and the ticket ID ends up in the bytes.
        let text = String(decoding: try make().payloadData(), as: UTF8.self)
        for forbidden in ["Kjetil", "sender", "avsender", "message", "grunn", "name", "navn"] {
            XCTAssertFalse(text.lowercased().contains(forbidden.lowercased()), "payload must not contain \(forbidden)")
        }
    }

    func testHeadersFollowTheContract() throws {
        let push = try make()
        let request = try push.urlRequest(authToken: "jwt")
        XCTAssertEqual(request.url?.absoluteString, "https://api.sandbox.push.apple.com/3/device/\(Self.token)")
        XCTAssertEqual(request.httpMethod, "POST")
        XCTAssertEqual(request.value(forHTTPHeaderField: "apns-push-type"), "alert")
        XCTAssertEqual(request.value(forHTTPHeaderField: "apns-priority"), "10")
        XCTAssertEqual(request.value(forHTTPHeaderField: "apns-topic"), "org.digipomps.haven")
        XCTAssertEqual(request.value(forHTTPHeaderField: "apns-collapse-id"), Self.ticketID)
        XCTAssertEqual(request.value(forHTTPHeaderField: "authorization"), "bearer jwt")
        XCTAssertEqual(request.httpBody, try push.payloadData())
    }

    func testProductionEnvironmentUsesProductionHost() throws {
        let request = try make(environment: .production).urlRequest(authToken: "jwt")
        XCTAssertEqual(request.url?.host, "api.push.apple.com")
    }

    func testExpirationIsMinOfTicketExpiryAndFourteenDays() throws {
        let now = Int(Self.now.timeIntervalSince1970)
        XCTAssertEqual(try make(ticketExpiresAt: now + 3_600).expiration, now + 3_600)
        XCTAssertEqual(try make(ticketExpiresAt: now + 90 * 86_400).expiration, now + 14 * 86_400)
        let header = try make(ticketExpiresAt: now + 3_600).headers["apns-expiration"]
        XCTAssertEqual(header, String(now + 3_600))
    }

    func testRefusesMalformedInput() {
        XCTAssertThrowsError(try make(ticketID: "")) { XCTAssertEqual($0 as? InviteApnsFailure, .badTicketID) }
        XCTAssertThrowsError(try make(ticketID: String(repeating: "a", count: 65))) { XCTAssertEqual($0 as? InviteApnsFailure, .badTicketID) }
        XCTAssertThrowsError(try make(ticketID: "inv 1\"}")) { XCTAssertEqual($0 as? InviteApnsFailure, .badTicketID) }
        XCTAssertThrowsError(try make(token: "XYZ")) { XCTAssertEqual($0 as? InviteApnsFailure, .badToken) }
        XCTAssertThrowsError(try make(token: String(repeating: "A", count: 64))) { XCTAssertEqual($0 as? InviteApnsFailure, .badToken) }
        XCTAssertThrowsError(try make(bundleID: "a/b")) { XCTAssertEqual($0 as? InviteApnsFailure, .badBundleID) }
    }

    func testRealTicketIDShapeFitsComfortably() throws {
        // invite.prepare mints "inv-" + lowercase UUID (40 bytes).
        let id = "inv-" + UUID().uuidString.lowercased()
        XCTAssertTrue(InviteApnsPush.isValidTicketID(id))
        XCTAssertLessThan(try make(ticketID: id).payloadData().count, InviteApnsPush.maxPayloadBytes)
    }

    // MARK: adapter

    func testAdapterSendsInviteThroughTransportAndSurfacesRejection() async throws {
        let transport = InviteCapturingTransport(responses: [
            .init(statusCode: 200, headers: ["apns-id": "apns-1"], body: Data()),
            .init(statusCode: 410, headers: [:], body: Data(#"{"reason":"Unregistered"}"#.utf8))
        ])
        let provider = APNSPushProviderAdapter(
            configuration: try XCTUnwrap(APNSPushConfiguration(environment: [
                "APNS_TEAM_ID": "TEAM123456",
                "APNS_KEY_ID": "KEY1234567",
                "APNS_PRIVATE_KEY_P8": Self.testPrivateKey,
                "APNS_BUNDLE_ID": "ignored.for.invites"
            ])),
            transport: transport
        )
        let push = try make()

        let ok = try await provider.sendInvite(push)
        XCTAssertTrue(ok.accepted)
        XCTAssertEqual(ok.providerMessageID, "apns-1")

        let refused = try await provider.sendInvite(push)
        XCTAssertFalse(refused.accepted)
        XCTAssertTrue((refused.diagnosticMessage ?? "").contains("Unregistered"))

        let sent = await transport.requests()
        XCTAssertEqual(sent.count, 2)
        let first = try XCTUnwrap(sent.first)
        XCTAssertEqual(first.url?.host, "api.sandbox.push.apple.com")
        XCTAssertEqual(first.value(forHTTPHeaderField: "apns-topic"), "org.digipomps.haven", "topic comes from the registration, not the scaffold's env")
        XCTAssertTrue((first.value(forHTTPHeaderField: "authorization") ?? "").hasPrefix("bearer "))
        XCTAssertEqual(first.httpBody, try push.payloadData())
    }

    private static let testPrivateKey = """
    -----BEGIN PRIVATE KEY-----
    MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgUC6oOLmd9F3Ak32L
    WJCzQB1eF00UX5MCzYi47hNS+zqhRANCAASWIbQJIqS1L1E8G2Z5uNSPgQGZcsfz
    xk1shW3jTkWmRWY3MSr+CumivsCLz0YR4OkIHm8SAxGomGYF1dO0skj4
    -----END PRIVATE KEY-----
    """
}

private actor InviteCapturingTransport: PushHTTPTransport {
    private var responses: [PushHTTPResponse]
    private var captured: [URLRequest] = []
    init(responses: [PushHTTPResponse]) { self.responses = responses }
    func send(_ request: URLRequest) async throws -> PushHTTPResponse {
        captured.append(request)
        guard !responses.isEmpty else { throw URLError(.badServerResponse) }
        return responses.removeFirst()
    }
    func requests() -> [URLRequest] { captured }
}
