# Dataflow — native-porthole/session (fase 2)

| # | Fra → Til | Kant (endepunkt/event) | Kontrakt/kilde |
|---|---|---|---|
| 1 | Klient-resolver → vert | `GET wss://<host>/v1/resolver/native-porthole/<pubId>/session` (upgrade) med sesjonskontrakt i query (`contract_payload_b64url` + sha256, som i dag) | `remoteMultiplexSessionURL` (`CellResolver.swift:2216`); `SproutResolverCompatibility.swift:839` |
| 2 | `shouldUpgrade` → aksept/avslag | Dagens kjede (signatur, expiry, issuer, `bridge_endpoint`, publisher-allowlist) **+ scope-krav**: uten `scope` → `sessionScopeMissing` | `bridge_session_handshake_contract_v1.json` §session |
| 3 | Socket → `BridgeMultiplexServerSession` | Én fysisk transport, sterk referanse i sesjonsregister (fase 1-mønsteret) | `AdminScaffoldBridgeRoutes.swift:28` (mønster) |
| 4 | Klient → vert | `openChannel(targetEndpoint[, actorCell?])` | kontrakt §channelOpen |
| 5 | `channelFactory` → kanal | Authz per åpning: `publishedCellName ∈ scope.channels`, kanaltall ≤ min(scope.channelCap, 64) → `BridgeBase` inbound + navngitt emit-celle per kanal; ellers `channelRejected(kode)`, øvrige kanaler lever | kontrakt §channelOpen.validation |
| 6 | Kanal → celle | Emit/Meddle gjennom `BridgeMultiplexChannelTransport` — uendret semantikk | `BridgeMultiplexing.swift` |
| 7 | Klient → vert | `closeChannel` → WP2-hook → avregistrer kanalens emit-celle | WP2 (ny hook) |
| 8 | Socket-tap → alle kanaler | Eksplisitt closed-signal til hver kanaldelegat; register slipper sesjonen; klienten bygger broene på nytt; `resumeFromSequence` finnes ikke lenger | WP2; beslutning 04.09 |
| 9 | Transport-oppsettsfeil → kanaler | `sendSetValueState` fannes ut til alle aktive kanaldelegater | WP2 |
