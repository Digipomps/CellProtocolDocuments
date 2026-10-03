// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

//
//  VaporInviteLanding.swift
//  CellScaffold
//
//  The other end of an invitation.
//
//  Someone who has never heard of HAVEN taps a link in an e-mail. What they
//  get is one page, server-rendered, no JavaScript required, that says who
//  invited them, what the link does, what it does not do, and offers one next
//  step. Everything else here exists to serve that page honestly.
//
//  Two properties this file is careful about:
//
//  **It is not an oracle.** A short code is a guessable six characters, so the
//  short-code path answers "not available" identically for unknown, expired
//  and withdrawn, and is rate limited. A self-contained token is different:
//  whoever holds it already has every fact inside it, so being specific there
//  reveals nothing they did not bring with them.
//
//  **It holds no authority.** The verdict comes from `HavenInviteVerifier` in
//  CellBase — the same code Binding runs — so a ticket cannot mean one thing
//  here and another in the app. The scaffold cannot mint, alter or approve an
//  invitation; it stores what an issuer signed and counts what happened.
//

import Foundation
import Fluent
import Vapor
@preconcurrency import CellBase

struct VaporInviteLanding: RouteCollection {

    /// Short codes are guessable, so treat lookups like login attempts.
    private static let shortCodePolicy = AuthRateLimiter.Policy(
        windowSeconds: 10 * 60,
        maxAttempts: 20,
        blockSeconds: 15 * 60
    )
    /// Replies are cheap to send and expensive to receive.
    private static let replyPolicy = AuthRateLimiter.Policy(
        windowSeconds: 10 * 60,
        maxAttempts: 8,
        blockSeconds: 30 * 60
    )

    func boot(routes: any RoutesBuilder) throws {
        let invite = routes.grouped(PathComponent(stringLiteral: HavenInviteLink.pathSegment))

        // Issuer-side API. Every call is either signed or presents the status
        // key minted at publication.
        let api = invite.grouped("api")
        api.post("publish", use: publish)
        api.post("revoke", use: revoke)
        api.post("status", use: status)
        api.post("requests", use: requests)

        // The page itself.
        invite.get(":token", use: landing)
        invite.post(":token", "reply", use: reply)
    }

    // MARK: - Issuer API

    /// Registers a ticket the issuer already signed.
    ///
    /// The scaffold verifies three things it can check on its own: that the
    /// enclosed ticket's signature holds, that the publication describes that
    /// exact ticket, and that the publication is signed by the same identity.
    /// Together those stop someone who intercepted a link from re-publishing
    /// it under a code they control.
    private func publish(req: Request) async throws -> Response {
        let publication = try req.content.decode(HavenInvitePublication.self)

        let ticket: HavenInviteTicket
        do {
            ticket = try HavenInvitePublicationVerifier.verifyPublication(publication)
        } catch let failure as HavenInvitePublicationVerifier.Failure {
            return try Self.json(status: .forbidden, ["code": failure.code, "message": failure.description])
        } catch let failure as HavenInviteLink.Failure {
            return try Self.json(status: .badRequest, ["code": failure.code, "message": failure.description])
        }

        guard !ticket.isExpired() else {
            return try Self.json(status: .badRequest, [
                "code": "expired",
                "message": "Billetten er allerede utløpt."
            ])
        }

        if let existing = try await InviteTicketRecord.query(on: req.db)
            .filter(\.$ticketID == publication.ticketID)
            .first() {
            // Re-publishing the same ticket is idempotent; re-publishing a
            // different one under the same id is not.
            guard existing.ticketToken == publication.ticketToken else {
                return try Self.json(status: .conflict, [
                    "code": "already_published",
                    "message": "En annen billett er allerede registrert med den id-en."
                ])
            }
            return try Self.json(status: .ok, ["code": "ok", "message": "Allerede registrert."])
        }

        if try await InviteTicketRecord.query(on: req.db)
            .filter(\.$humanCode == publication.humanCode)
            .first() != nil {
            return try Self.json(status: .conflict, [
                "code": "code_taken",
                "message": "Koden er allerede i bruk. Lag en ny invitasjon."
            ])
        }

        let record = InviteTicketRecord(
            ticketID: publication.ticketID,
            humanCode: publication.humanCode,
            ticketToken: publication.ticketToken,
            audienceToken: publication.audienceToken,
            issuerIdentityUUID: publication.issuerIdentityUUID,
            issuerDisplayName: ticket.issuerDisplayName,
            statusKey: publication.statusKey,
            expiresAt: ticket.expiryDate,
            maxContactRequests: max(1, min(20, publication.maxContactRequests))
        )
        try await record.save(on: req.db)

        return try Self.json(status: .ok, [
            "code": "ok",
            "message": "Registrert.",
            "humanCode": publication.humanCode
        ])
    }

    /// Withdrawal. Signed by the issuer and checked against the stored ticket,
    /// so knowing a ticket id is not enough to cancel someone's invitation.
    private func revoke(req: Request) async throws -> Response {
        let notice = try req.content.decode(HavenInviteRevocationNotice.self)

        guard let record = try await InviteTicketRecord.query(on: req.db)
            .filter(\.$ticketID == notice.ticketID)
            .first() else {
            return try Self.json(status: .notFound, ["code": "not_found", "message": "Ukjent billett."])
        }

        let ticket: HavenInviteTicket
        do {
            ticket = try HavenInviteLink.decode(record.ticketToken)
            try HavenInvitePublicationVerifier.verifyRevocation(notice, againstIssuerOf: ticket)
        } catch let failure as HavenInvitePublicationVerifier.Failure {
            return try Self.json(status: .forbidden, ["code": failure.code, "message": failure.description])
        } catch {
            return try Self.json(status: .badRequest, ["code": "bad_request", "message": "Ugyldig tilbakekalling."])
        }

        record.revokedAt = Date()
        record.revocationReason = String(notice.reason.prefix(240))
        try await record.save(on: req.db)

        return try Self.json(status: .ok, ["code": "ok", "message": "Trukket tilbake."])
    }

    private struct StatusQuery: Content {
        var ticketID: String
        var statusKey: String
    }

    /// The issuer reading their own funnel. The status key is the whole
    /// authorisation: without it this endpoint would answer "has anyone opened
    /// invitation X" for anybody who could guess an id.
    private func status(req: Request) async throws -> Response {
        let query = try req.content.decode(StatusQuery.self)
        guard let record = try await authorisedRecord(req: req, query: query) else {
            return try Self.json(status: .notFound, ["code": "not_found", "message": "Ukjent billett."])
        }
        let report = HavenInviteStatusReport(
            ticketID: record.ticketID,
            state: record.lifecycle(),
            firstOpenedAt: record.firstOpenedAt.map { Int($0.timeIntervalSince1970) },
            openCount: record.openCount,
            respondedAt: record.respondedAt.map { Int($0.timeIntervalSince1970) },
            contactRequestCount: try await InviteContactRequestRecord.query(on: req.db)
                .filter(\.$ticketID == record.ticketID)
                .count(),
            resultingEntityRef: record.resultingEntityRef
        )
        return try Self.json(status: .ok, report)
    }

    private struct ContactRequestEnvelope: Content {
        var requests: [HavenInviteContactRequest]
    }

    /// Collecting replies. Delivered once and marked collected — the scaffold
    /// is a mailbox, not an archive of other people's introductions.
    private func requests(req: Request) async throws -> Response {
        let query = try req.content.decode(StatusQuery.self)
        guard let record = try await authorisedRecord(req: req, query: query) else {
            return try Self.json(status: .notFound, ["code": "not_found", "message": "Ukjent billett."])
        }

        let payloadJSONs = try await InviteLandingRetention.collectUncollectedPayloads(
            ticketID: record.ticketID,
            on: req.db
        )
        let decoder = JSONDecoder()
        var payloads: [HavenInviteContactRequest] = []
        for payloadJSON in payloadJSONs {
            guard let data = payloadJSON.data(using: .utf8),
                  let request = try? decoder.decode(HavenInviteContactRequest.self, from: data) else { continue }
            payloads.append(request)
        }

        return try Self.json(status: .ok, ContactRequestEnvelope(requests: payloads))
    }

    private func authorisedRecord(req: Request, query: StatusQuery) async throws -> InviteTicketRecord? {
        guard let record = try await InviteTicketRecord.query(on: req.db)
            .filter(\.$ticketID == query.ticketID)
            .first() else { return nil }
        // Same answer for "wrong key" and "no such ticket", so the endpoint
        // cannot be used to confirm that an id exists.
        guard record.matchesStatusKey(query.statusKey) else { return nil }
        return record
    }

    // MARK: - The page

    private func landing(req: Request) async throws -> Response {
        guard let raw = req.parameters.get("token")?.trimmingCharacters(in: .whitespacesAndNewlines),
              !raw.isEmpty, raw.count <= 4096 else {
            throw Abort(.notFound)
        }

        let isShortCode = HavenInviteLink.looksLikeHumanCode(raw)
        if isShortCode {
            let key = "invite-code:\(req.remoteAddress?.ipAddress ?? "unknown")"
            if let retryAfter = await req.authRateLimiter.recordAttempt(key: key, policy: Self.shortCodePolicy) {
                return Self.html(
                    status: .tooManyRequests,
                    InviteLandingHTML.renderUnavailable(
                        headline: "Vent litt",
                        detail: "For mange forsøk fra denne maskinen. Prøv igjen om \(max(1, retryAfter / 60)) minutter."
                    )
                )
            }
        }

        // Resolve to a ticket: a code needs the stored row, a token carries
        // itself and only needs the row for revocation state.
        var record: InviteTicketRecord?
        let ticket: HavenInviteTicket
        if isShortCode {
            guard let stored = try await InviteTicketRecord.query(on: req.db)
                .filter(\.$humanCode == raw.uppercased())
                .first(),
                let decoded = try? HavenInviteLink.decode(stored.ticketToken) else {
                // Deliberately identical for unknown / expired / withdrawn.
                return Self.html(status: .notFound, InviteLandingHTML.renderUnavailable(
                    headline: "Invitasjonen er ikke tilgjengelig",
                    detail: "Koden finnes ikke, eller invitasjonen er ikke lenger aktiv. Be den som inviterte deg om en ny."
                ))
            }
            record = stored
            ticket = decoded
        } else {
            do {
                ticket = try HavenInviteLink.decode(raw)
            } catch let failure as HavenInviteLink.Failure {
                return Self.html(status: .badRequest, InviteLandingHTML.renderUnavailable(
                    headline: "Denne lenken ser ikke riktig ut",
                    detail: failure.description
                ))
            }
            record = try await InviteTicketRecord.query(on: req.db)
                .filter(\.$ticketID == ticket.ticketID)
                .first()
        }

        let revoked: Set<String> = (record?.isRevoked == true) ? [ticket.ticketID] : []
        let verdict = HavenInviteVerifier.verify(ticket: ticket, revokedTicketIDs: revoked)

        // Count the open before rendering, and only once per ticket for the
        // first-open timestamp. This is the first honest signal in the funnel;
        // everything before publication was self-reported.
        if let record, verdict.isValid {
            record.openCount += 1
            if record.firstOpenedAt == nil { record.firstOpenedAt = Date() }
            try? await record.save(on: req.db)
        }

        guard verdict.isValid else {
            if isShortCode {
                return Self.html(status: .gone, InviteLandingHTML.renderUnavailable(
                    headline: "Invitasjonen er ikke tilgjengelig",
                    detail: "Koden finnes ikke, eller invitasjonen er ikke lenger aktiv. Be den som inviterte deg om en ny."
                ))
            }
            // The holder of a self-contained token already has every fact in
            // it, so the precise reason tells them nothing new.
            return Self.html(status: .gone, InviteLandingHTML.renderUnavailable(
                headline: "Denne invitasjonen kan ikke brukes",
                detail: verdict.reason
            ))
        }

        let signedIn = (try? req.auth.require(FidoUser.self)) != nil
        let replied = req.query[String.self, at: "replied"] == "1"
        return Self.html(status: .ok, InviteLandingHTML.render(
            ticket: ticket,
            verdict: verdict,
            token: raw,
            isPublished: record != nil,
            signedIn: signedIn,
            replySent: replied
        ))
    }

    // MARK: - Replying

    private struct ReplyForm: Content {
        var displayName: String?
        var message: String?
    }

    /// The reply, from either side of the fence.
    ///
    /// An app that already has an identity posts a signed
    /// `HavenInviteContactRequest` as JSON and the scaffold just checks and
    /// stores it. A person on the web has no signing identity until they have
    /// signed in, so the form path requires a session and refuses politely
    /// rather than storing something nobody can verify.
    private func reply(req: Request) async throws -> Response {
        guard let raw = req.parameters.get("token"), !raw.isEmpty else { throw Abort(.notFound) }

        let key = "invite-reply:\(req.remoteAddress?.ipAddress ?? "unknown")"
        if let retryAfter = await req.authRateLimiter.recordAttempt(key: key, policy: Self.replyPolicy) {
            return try Self.json(status: .tooManyRequests, [
                "code": "rate_limited",
                "message": "For mange forsøk. Prøv igjen om \(max(1, retryAfter / 60)) minutter."
            ])
        }

        // JSON path: a signed request from an app.
        if req.headers.contentType?.type == "application" && req.headers.contentType?.subType == "json",
           let request = try? req.content.decode(HavenInviteContactRequest.self) {
            return try await store(request: request, req: req)
        }

        // Form path: a person in a browser.
        guard (try? req.auth.require(FidoUser.self)) != nil else {
            let next = "/\(HavenInviteLink.pathSegment)/\(raw)"
            return req.redirect(to: "/login?next=\(next.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? next)")
        }
        return try Self.json(status: .notImplemented, [
            "code": "web_reply_pending",
            "message": "Svar fra nettleseren krever at scaffoldet signerer på dine vegne. Det er ikke koblet opp ennå — bruk HAVEN-appen, eller be avsenderen kontakte deg direkte."
        ])
    }

    private func store(request: HavenInviteContactRequest, req: Request) async throws -> Response {
        guard let record = try await InviteTicketRecord.query(on: req.db)
            .filter(\.$ticketID == request.ticketID)
            .first() else {
            return try Self.json(status: .notFound, ["code": "not_found", "message": "Ukjent billett."])
        }
        guard !record.isRevoked, !record.isExpired() else {
            return try Self.json(status: .gone, [
                "code": "not_active",
                "message": "Invitasjonen er ikke lenger aktiv."
            ])
        }

        let ticket: HavenInviteTicket
        do {
            ticket = try HavenInviteLink.decode(record.ticketToken)
            try HavenInvitePublicationVerifier.verifyContactRequest(request, forTicket: ticket)
        } catch let failure as HavenInvitePublicationVerifier.Failure {
            return try Self.json(status: .forbidden, ["code": failure.code, "message": failure.description])
        } catch {
            return try Self.json(status: .badRequest, ["code": "bad_request", "message": "Ugyldig forespørsel."])
        }

        // A forwarded link must not become an open inbox.
        let existing = try await InviteContactRequestRecord.query(on: req.db)
            .filter(\.$ticketID == record.ticketID)
            .count()
        guard existing < record.maxContactRequests else {
            return try Self.json(status: .conflict, [
                "code": "inbox_full",
                "message": "Denne invitasjonen har allerede tatt imot så mange svar som den kan."
            ])
        }
        if try await InviteContactRequestRecord.query(on: req.db)
            .filter(\.$requestID == request.requestID)
            .first() != nil {
            return try Self.json(status: .ok, ["code": "ok", "message": "Allerede mottatt."])
        }

        guard let payload = try? JSONEncoder().encode(request),
              let json = String(data: payload, encoding: .utf8) else {
            return try Self.json(status: .badRequest, ["code": "bad_request", "message": "Kunne ikke lagre forespørselen."])
        }

        try await InviteContactRequestRecord(
            requestID: request.requestID,
            ticketID: record.ticketID,
            payloadJSON: json,
            senderDisplayName: String(request.senderDisplayName.prefix(120))
        ).save(on: req.db)

        record.respondedAt = Date()
        record.resultingEntityRef = request.senderEntityRef
        try await record.save(on: req.db)

        return try Self.json(status: .ok, [
            "code": "ok",
            "message": "Svaret er levert. \(ticket.issuerDisplayName) henter det neste gang HAVEN er åpen."
        ])
    }

    // MARK: - Responses

    private static func html(status: HTTPStatus, _ body: String) -> Response {
        Response(
            status: status,
            headers: [
                "content-type": "text/html; charset=utf-8",
                // Nothing on this page should be cached by a shared proxy.
                "cache-control": "no-store",
                "referrer-policy": "no-referrer"
            ],
            body: .init(string: body)
        )
    }

    private static func json(status: HTTPStatus, _ payload: [String: String]) throws -> Response {
        let data = try JSONEncoder().encode(payload)
        return Response(
            status: status,
            headers: ["content-type": "application/json; charset=utf-8", "cache-control": "no-store"],
            body: .init(data: data)
        )
    }

    private static func json(status: HTTPStatus, _ payload: some Encodable) throws -> Response {
        let data = try JSONEncoder().encode(payload)
        return Response(
            status: status,
            headers: ["content-type": "application/json; charset=utf-8", "cache-control": "no-store"],
            body: .init(data: data)
        )
    }
}
