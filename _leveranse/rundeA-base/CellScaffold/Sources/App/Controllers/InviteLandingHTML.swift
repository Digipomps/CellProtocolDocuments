// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

//
//  InviteLandingHTML.swift
//  CellScaffold
//
//  The page a person who has never heard of HAVEN sees first.
//
//  Server-rendered, no JavaScript, one screen. The whole design problem here
//  is that honesty and persuasion pull in opposite directions: the truthful
//  sentence about this link is "it gives you nothing of mine", which is not by
//  itself a reason to click. So the page leads with the one thing that *is*
//  concrete — a named person you know asked for you, and you can answer them —
//  and puts the boundary right next to it rather than hiding it below a fold.
//
//  Deliberately absent: a countdown, a progress bar, "join 10 000 others", or
//  anything else that implies momentum we do not have. Overclaiming here would
//  be the first thing HAVEN ever said to this person.
//

import Foundation
@preconcurrency import CellBase

enum InviteLandingHTML {

    static func render(
        ticket: HavenInviteTicket,
        verdict: HavenInviteVerifier.Verdict,
        token: String,
        isPublished: Bool,
        signedIn: Bool,
        replySent: Bool
    ) -> String {
        let issuer = escape(ticket.issuerDisplayName)
        let greeting = ticket.greetingName.map { "Hei \(escape($0))," } ?? "Hei,"
        let note = ticket.note.map {
            "<blockquote class=\"note\">\(escape($0))</blockquote>"
        } ?? ""

        let canReply = ticket.canReceiveContactRequest
        let replyPanel = replySent
            ? """
              <section class="panel done" role="status">
                <h2>Svaret er levert</h2>
                <p>\(issuer) henter det neste gang HAVEN er åpen hos hen.</p>
              </section>
              """
            : (canReply ? replyForm(token: token, issuer: issuer, signedIn: signedIn) : "")

        let expiry = readable(ticket.expiryDate)

        return page(
            title: "\(issuer) inviterer deg · HAVEN",
            body: """
            <section class="hero">
              <p class="eyebrow">Invitasjon</p>
              <h1>\(issuer) vil ha deg med i HAVEN</h1>
              <p class="purpose">\(greeting) \(issuer) bruker HAVEN og har sendt deg denne lenken personlig.</p>
              \(note)
              <div class="trust">
                <div><strong>Du oppretter din egen konto.</strong> Du velger selv hva du legger inn og deler videre.</div>
                <div><strong>\(issuer) får ikke konto- eller innholdsdata.</strong> Bare navn og melding hvis du selv velger å svare.</div>
                <div><strong>Lenken gir ikke tilgang til \(issuer) sitt innhold.</strong> Den bekrefter bare den signerte invitasjonen.</div>
              </div>
            </section>

            <section class="panel">
              <h2>Neste steg</h2>
              <p>Opprett din egen HAVEN. Det tar ett steg, og du bestemmer selv hva du legger inn etterpå.</p>
              <a class="cta" href="/login?next=\(escapeAttribute(nextPath(token)))">Opprett din egen HAVEN</a>
              <p class="fine">Har du HAVEN fra før? <a href="haven://invite/\(escapeAttribute(token))">Åpne invitasjonen i appen</a>.</p>
            </section>

            \(replyPanel)

            <section class="panel muted">
              <h2>Om denne lenken</h2>
              <ul class="facts">
                <li>Kode: <code>\(escape(ticket.humanCode))</code></li>
                <li>Gyldig til \(escape(expiry))</li>
                <li>Signert av \(issuer) — vi har sjekket signaturen på denne siden</li>
                \(isPublished ? "" : "<li>Denne lenken bærer hele invitasjonen selv, og er ikke registrert hos oss</li>")
              </ul>
              <p class="fine">\(escape(HavenInviteCopy.boundary(for: ticket)))</p>
            </section>

            <section class="panel muted">
              <h2>Hva er HAVEN?</h2>
              <p>
                HAVEN undersøker hvordan mennesker kan få mer synlig kontroll over data,
                relasjoner, formål og avtaler i digitale tjenester. Dette er en tidlig pilot:
                funksjonene og lagringsgrensene er fortsatt under utvikling.
              </p>
            </section>
            """
        )
    }

    static func renderUnavailable(headline: String, detail: String) -> String {
        page(
            title: "Invitasjon · HAVEN",
            body: """
            <section class="hero">
              <p class="eyebrow">Invitasjon</p>
              <h1>\(escape(headline))</h1>
              <p class="purpose">\(escape(detail))</p>
            </section>
            <section class="panel muted">
              <p class="fine">
                Siden bruker ingen annonse- eller tredjepartssporing. Tjenesten kan behandle
                nettverksadressen i minnet for misbruksvern, og en gyldig publisert invitasjon
                får et begrenset åpningstall.
              </p>
            </section>
            """
        )
    }

    // MARK: - Pieces

    private static func replyForm(token: String, issuer: String, signedIn: Bool) -> String {
        guard signedIn else {
            return """
            <section class="panel">
              <h2>Vil du bare svare \(issuer)?</h2>
              <p>Du kan sende en kontaktforespørsel tilbake uten å bygge noe mer. Det krever at du oppretter din egen HAVEN først, så svaret blir signert av deg og ikke av oss.</p>
              <a class="cta secondary" href="/login?next=\(escapeAttribute(nextPath(token)))">Opprett konto og svar</a>
            </section>
            """
        }
        return """
        <section class="panel">
          <h2>Svar \(issuer)</h2>
          <form method="post" action="/\(HavenInviteLink.pathSegment)/\(escapeAttribute(token))/reply">
            <label for="message">Melding (valgfritt)</label>
            <textarea id="message" name="message" maxlength="600" placeholder="Hei! Ja, jeg er nysgjerrig."></textarea>
            <button type="submit">Send kontaktforespørsel</button>
          </form>
          <p class="fine">\(issuer) ser navnet ditt og meldingen. Ingenting annet følger med.</p>
        </section>
        """
    }

    private static func nextPath(_ token: String) -> String {
        "/\(HavenInviteLink.pathSegment)/\(token)"
    }

    private static func page(title: String, body: String) -> String {
        """
        <!doctype html>
        <html lang="no">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <meta name="color-scheme" content="light dark">
          <meta name="robots" content="noindex, nofollow">
          <meta name="referrer" content="no-referrer">
          <title>\(title)</title>
          <style>
            :root { color-scheme: light; --ink:#10251f; --soft:#52665f; --paper:#f8fbf9; --line:#dce8e2; --accent:#087f5b; --warm:#fff7df; }
            * { box-sizing:border-box; }
            body { margin:0; min-height:100vh; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color:var(--ink); background:radial-gradient(circle at 10% 0%,#dff7eb 0,transparent 34rem),linear-gradient(145deg,#f8fbf9,#edf5f1); }
            main { width:min(720px,calc(100% - 32px)); margin:0 auto; padding:42px 0 64px; }
            .brand { display:flex; align-items:center; gap:10px; margin-bottom:32px; font-weight:750; letter-spacing:.08em; }
            .mark { width:34px; height:34px; display:grid; place-items:center; border-radius:12px; color:white; background:linear-gradient(145deg,#0b9b70,#075b46); box-shadow:0 8px 24px #087f5b33; }
            .hero,.panel { border:1px solid var(--line); border-radius:24px; background:#ffffffde; box-shadow:0 18px 60px #183c2e12; }
            .hero { padding:clamp(26px,6vw,48px); }
            .panel { margin-top:18px; padding:clamp(22px,4vw,32px); }
            .panel.muted { background:#ffffffaa; }
            .panel.done { border-color:#0b9b70; }
            .eyebrow { margin:0 0 12px; color:var(--accent); font-weight:700; font-size:.82rem; text-transform:uppercase; letter-spacing:.08em; }
            h1 { max-width:20ch; margin:0; font-size:clamp(1.9rem,6vw,3.4rem); line-height:1.05; letter-spacing:-.03em; }
            h2 { margin:0 0 10px; font-size:1.18rem; }
            p { line-height:1.6; }
            .purpose { margin:22px 0 0; font-size:clamp(1.05rem,2.6vw,1.3rem); }
            .note { margin:20px 0 0; padding:16px 18px; border-left:4px solid var(--accent); border-radius:0 14px 14px 0; background:var(--warm); font-style:italic; }
            .trust { display:grid; grid-template-columns:1fr; gap:10px; margin-top:26px; }
            @media (min-width:640px) { .trust { grid-template-columns:repeat(3,1fr); } }
            .trust div { padding:14px; border:1px solid var(--line); border-radius:14px; background:var(--paper); font-size:.92rem; line-height:1.45; }
            .cta { display:inline-block; margin-top:8px; padding:14px 22px; border-radius:999px; background:var(--accent); color:white; font-weight:700; text-decoration:none; }
            .cta.secondary { background:#0f766e; }
            .cta:focus,button:focus,a:focus,textarea:focus { outline:3px solid #71d8b3; outline-offset:2px; }
            .fine { margin-top:14px; color:var(--soft); font-size:.9rem; }
            .facts { margin:0; padding-left:1.1rem; color:var(--soft); line-height:1.8; }
            code { padding:2px 7px; border-radius:6px; background:var(--paper); border:1px solid var(--line); letter-spacing:.14em; font-weight:700; color:var(--ink); }
            label { display:block; margin:12px 0 6px; font-weight:700; }
            textarea { width:100%; min-height:120px; padding:13px 14px; border:1px solid #b9ccc4; border-radius:13px; background:white; color:var(--ink); font:inherit; resize:vertical; }
            button { margin-top:14px; padding:13px 22px; border:0; border-radius:999px; background:var(--accent); color:white; font:inherit; font-weight:700; cursor:pointer; }
            @media (prefers-color-scheme: dark) {
              :root { color-scheme: dark; --ink:#e8f3ee; --soft:#9ab3aa; --paper:#12211c; --line:#26443a; --warm:#2a2617; }
              body { background:linear-gradient(145deg,#0c1714,#0f201a); }
              .hero,.panel { background:#12211ccc; box-shadow:none; }
              .panel.muted { background:#12211c99; }
              textarea { background:#0f1c18; border-color:#2c5347; }
            }
          </style>
        </head>
        <body>
          <main>
            <div class="brand"><span class="mark" aria-hidden="true">H</span><span>HAVEN</span></div>
            \(body)
          </main>
        </body>
        </html>
        """
    }

    // MARK: - Escaping

    /// Everything interpolated into this page came from someone else's signed
    /// ticket. The signature proves who wrote it, not that it is safe to
    /// render, so every field goes through here.
    static func escape(_ text: String) -> String {
        text
            .replacingOccurrences(of: "&", with: "&amp;")
            .replacingOccurrences(of: "<", with: "&lt;")
            .replacingOccurrences(of: ">", with: "&gt;")
            .replacingOccurrences(of: "\"", with: "&quot;")
            .replacingOccurrences(of: "'", with: "&#39;")
    }

    static func escapeAttribute(_ text: String) -> String {
        escape(text).replacingOccurrences(of: " ", with: "%20")
    }

    private static func readable(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "nb_NO")
        formatter.dateStyle = .long
        formatter.timeStyle = .none
        return formatter.string(from: date)
    }
}
