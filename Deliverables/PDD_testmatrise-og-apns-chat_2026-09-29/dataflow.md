# Dataflyt — testmatrise og APNs-chat

Last verified against code: 2026-10-06 (kanter som peker på eksisterende kode er lest fra `CellScaffold/Sources/App/Cells/ConferenceMVP/Notifications/PushProviderAdapter.swift`, `Binding/Binding/NotificationEnrollmentManager.swift`, `CellProtocol/Sources/CellBase/Invitation/*`). Alt merket **ny** er planlagt, ikke implementert.

## Kantene

| # | Fra → Til | Hva går | Kontrakt | Finnes i dag? |
|---|---|---|---|---|
| E1 | iPhone-appen → Apple | `registerForRemoteNotifications` → enhets-token | Apple | ja (`NotificationEnrollmentManager`) |
| E2 | iPhone-appen → skyscaffold | `push.register`: entitet, miljø, bundle-ID, token, signert av entiteten | `apns_invite_v1#push.register` | **ny** (i dag: enhetsregistrering knyttet til konferanse) |
| E3 | iPhone-appen → skyscaffold | `push.revoke` | `apns_invite_v1#push.revoke` | **ny** |
| E4 | avsenders butler → skyscaffold | publisert billett (`HavenInvitePublication`, med valgfri signert `audienceEntity` — nytt felt) | invitasjons-PDD, WP2 | typer ja (#51); scaffold-siden **ikke** (runde A del 2) |
| E4b | invitasjonscelle → egne relasjoner / registre i andres scaffolds | oppslag av navn eller endepunkt → entitet (`audienceEntity`) eller «ikke funnet» | invitasjons-PDD WP13/14 + denne PDD-ens WP13 | **ny** (egne relasjoner: lokalt; andres registre: avhenger av invitasjons-PDD WP13/14) |
| E5 | skyscaffold (invitasjonscelle) → push-celle | `invite.push`: ticketID + `audienceEntity` (bare når E4b fant en entitet) | `apns_invite_v1#invite.push` | **ny** |
| E6 | push-celle → registerlager | slå opp aktiv registrering for audience | `#invite.push` (beslutning) | **ny** |
| E7 | push-celle → `HavenInviteVerifier` / `HavenInviteTombstoneLedger` | er billetten gyldig, ikke utløpt/trukket, ikke gravlagt | CellProtocol (#51) | ja (typene) |
| E8 | push-celle → `APNSPushProviderAdapter` | `PushSendRequest` med invitasjonspayload | `PushProviderAdapter.swift` | adapter ja; invitasjonspayload **ny** |
| E9 | adapter → `PushHTTPTransport` | HTTP/2 mot `api(.sandbox).push.apple.com` | Apple | ja; **stub-transport for test ny** |
| E10 | Apple → iPhone | varsel `{aps:{alert}, haven:{k,id}}` | `#invite.push.apns.payload` | Apple-siden utenfor vår kontroll |
| E11 | iPhone-appen → skyscaffold | `push.tap`: hent billett for ticketID (GET, som landing) | invitasjons-PDD (landing/GET) | **ny** (avhenger av runde A del 2) |
| E12 | iPhone-appen → `HavenInviteVerifier` | verifiser billetten lokalt | CellProtocol (#51) | ja |
| E13 | iPhone-appen → scaffold | ja/nei (reply) → aksept → to envelopes → ChatCell | invitasjons-PDD WP7/WP5 | **ikke gjort** |
| E14 | push-celle → scaffoldets interne logg | utfall `sent / wrong_audience / …` | `#invite.push.decision` | **ny** — aldri til avsender |

```
 avsender (butler) ──E4──▶ invitasjonscelle ──E5──▶ push-celle ──E6──▶ registerlager
                                                      │  ▲
                                                      │  └─E7── Verifier + gravsteinsregister
                                                      ├─E14─▶ intern logg  (ikke synlig for avsender)
                                                      └─E8──▶ APNSPushProviderAdapter ─E9─▶ transport ──▶ Apple ─E10─▶ iPhone
 iPhone ──E1──▶ Apple (token)         iPhone ──E2/E3──▶ registerlager (signert)
 iPhone ──(trykk)─E11──▶ scaffold: hent billett ──E12──▶ Verifier ──▶ invitasjonsflate ──E13──▶ ja → chat
```

## Det testene tar på

- Alle kanter merket **ny** har en rad i `contract/apns_invite_v1.json` og minst én positiv og én negativ fixture (§5 `test.cells.dataflow-matches-contracts`).
- E9 testes mot stub-transport (alle `test.apns.*` unntatt `real-sandbox-send`); bare T5.5 går mot Apple.
- E14 er en kant som *ikke* må ha noen utgående forbindelse til avsenderens flate: testes ved at avsenderoversikten (`HavenInviteSenderView`) gir samme resultat uansett push-utfall.
