// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

//
//  InviteApnsPush.swift
//  CellScaffold
//
//  The APNs notification for "you have an invitation" — contract apns_invite_v1.
//
//  A notification says that something exists. It never carries content: no
//  sender name, no message text, no grounds. The phone learns the ticket ID,
//  fetches the ticket over the same path the landing page uses and verifies it
//  itself (purpose://candidate.testmatrise.apns.payload-carries-no-content,
//  purpose://candidate.testmatrise.apns.tap-opens-the-invitation).
//
//  Pure value code: builds bytes and headers, sends nothing. The adapter
//  (APNSPushProviderAdapter.sendInvite) owns the network and the provider token.
//

import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking
#endif

enum InviteApnsEnvironment: String, Sendable, Equatable {
    case sandbox
    case production

    var host: String {
        switch self {
        case .sandbox: return "api.sandbox.push.apple.com"
        case .production: return "api.push.apple.com"
        }
    }
}

enum InviteApnsFailure: Error, Equatable, Sendable {
    case badTicketID
    case badToken
    case badBundleID
    case payloadTooLarge(Int)
    case cannotBuildURL
}

struct InviteApnsPush: Sendable, Equatable {

    /// Fixed text. Norwegian, because the notification is shown on the lock screen
    /// of a person whose language we do not know yet and must not guess from them.
    static let title = "HAVEN"
    static let bodyNb = "Du har en invitasjon å svare på."
    static let kind = "invite"
    static let maxPayloadBytes = 256
    static let maxLifetimeSeconds = 14 * 24 * 60 * 60

    let ticketID: String
    let environment: InviteApnsEnvironment
    let bundleID: String
    let token: String
    /// Seconds since epoch. Already clamped by `make`.
    let expiration: Int

    /// ticketID doubles as `apns-collapse-id`, which tolerates at most 64 bytes.
    static func isValidTicketID(_ value: String) -> Bool {
        guard (1...64).contains(value.utf8.count) else { return false }
        return value.utf8.allSatisfy { byte in
            (byte >= 0x30 && byte <= 0x39) || (byte >= 0x41 && byte <= 0x5A) ||
            (byte >= 0x61 && byte <= 0x7A) || byte == 0x2D || byte == 0x2E || byte == 0x5F
        }
    }

    static func isValidToken(_ value: String) -> Bool {
        guard (64...200).contains(value.utf8.count) else { return false }
        return value.utf8.allSatisfy { ($0 >= 0x30 && $0 <= 0x39) || ($0 >= 0x61 && $0 <= 0x66) }
    }

    static func isValidBundleID(_ value: String) -> Bool {
        guard (3...155).contains(value.utf8.count) else { return false }
        return value.utf8.allSatisfy { byte in
            (byte >= 0x30 && byte <= 0x39) || (byte >= 0x41 && byte <= 0x5A) ||
            (byte >= 0x61 && byte <= 0x7A) || byte == 0x2D || byte == 0x2E
        }
    }

    /// `ticketExpiresAt` is the ticket's own expiry; the push never outlives it and
    /// never lives longer than 14 days.
    static func make(
        ticketID: String,
        environment: InviteApnsEnvironment,
        bundleID: String,
        token: String,
        ticketExpiresAt: Int,
        now: Date = Date()
    ) throws -> InviteApnsPush {
        guard isValidTicketID(ticketID) else { throw InviteApnsFailure.badTicketID }
        guard isValidToken(token) else { throw InviteApnsFailure.badToken }
        guard isValidBundleID(bundleID) else { throw InviteApnsFailure.badBundleID }
        let nowSeconds = Int(now.timeIntervalSince1970)
        let expiration = min(ticketExpiresAt, nowSeconds + maxLifetimeSeconds)
        let push = InviteApnsPush(
            ticketID: ticketID, environment: environment, bundleID: bundleID,
            token: token, expiration: expiration
        )
        _ = try push.payloadData()   // fail early if it does not fit
        return push
    }

    /// Canonical bytes: sorted keys, no whitespace, no escaped slashes. Exactly what
    /// the golden fixture in contract/fixtures pins down.
    func payloadData() throws -> Data {
        let object: [String: Any] = [
            "aps": ["alert": ["title": Self.title, "body": Self.bodyNb]],
            "haven": ["k": Self.kind, "id": ticketID]
        ]
        let data = try JSONSerialization.data(
            withJSONObject: object,
            options: [.sortedKeys, .withoutEscapingSlashes]
        )
        guard data.count <= Self.maxPayloadBytes else {
            throw InviteApnsFailure.payloadTooLarge(data.count)
        }
        return data
    }

    /// Headers apart from `authorization`, which the adapter adds.
    var headers: [String: String] {
        [
            "content-type": "application/json",
            "apns-push-type": "alert",
            "apns-priority": "10",
            "apns-topic": bundleID,
            "apns-collapse-id": ticketID,
            "apns-expiration": String(expiration)
        ]
    }

    func urlRequest(authToken: String) throws -> URLRequest {
        guard let url = URL(string: "https://\(environment.host)/3/device/\(token)") else {
            throw InviteApnsFailure.cannotBuildURL
        }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.httpBody = try payloadData()
        for (name, value) in headers { request.setValue(value, forHTTPHeaderField: name) }
        request.setValue("bearer \(authToken)", forHTTPHeaderField: "authorization")
        return request
    }
}
