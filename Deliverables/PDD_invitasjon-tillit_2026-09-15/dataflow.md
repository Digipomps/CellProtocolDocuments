# Dataflyt — invitasjon → samtale

Last verified against code: 2026-09-23 (origin/main: CellProtocol a785dc7, Binding 8ce634f6,
CellScaffold 77a922bc). Kanter merket **ny** finnes ikke i dag og lages i PLAN-pakken som er nevnt.

```
 KJETIL (entitet K, Binding)                 SCAFFOLD (Kjetils, CellScaffold)              VEGAR
 ───────────────────────────                 ────────────────────────────────              ─────
 Butler ──(1)──► InvitationCell ──(2)──► /api/invite/publish ──► InviteTicketRecord
                  │                                                    │
                  │  invite.prepare / publish                          │ (3) GET /invite/:token ──────────► landing (nettleser)
                  │                                                    │                                      │
                  │                                                    │ (4) POST /invite/:token/reply ◄──────┘ decision + basis-krav
                  │                                                    │        (HavenInviteContactRequest | Tombstone ny)
                  │ (5) invite.refreshStatus / pullContactRequests     │
                  ◄────────────────────────────────────────────────────┘
                  │
                  │ (6) invite.acceptContactRequest
                  ▼
        EntityAnchor(K) ◄─(7a) batchPersist ─┐          (7b) batchPersist ──► EntityAnchor(V)   [app-vei: i Vegars app]
                                             │                                 EntityAnchor(V') [direkte-vei: på Kjetils scaffold, ny WP8]
                  (8) ChatInvitationArtifact ─┼──────────────────────────────► Vegars identitet
                                             │                                      │
                  ChatCell(K) ◄──(9) ChatInvitationAcceptance ──────────────────────┘
                  │
                  │ (10) meldinger, konvolutter per mottaker
                  ▼
        (11) entity.moveHome (ny, WP12): EntityAnchor(V') ──► EntityAnchor(V) + re-binding av ChatCell-medlemskap
```

## Kanter

| # | Fra → til | Endepunkt / hendelse | Bærer | Hvem ser hva | Kilde |
|---|---|---|---|---|---|
| 1 | Butler → InvitationCell | `invite.prepare` (via `acceptInviteSuggestion`) | kontaktpost `basis` (ikke `privateNotes` — **ny** skille, WP3/4), identityDomain (**ny**, WP1), hilsen, ttlDays | bare K | `Binding/ChatWorkbenchParityCells.swift`, `Cells/InvitationCell.swift` |
| 2 | InvitationCell → scaffold | `POST /api/invite/publish` | `HavenInvitePublication` (signert billett + statusnøkkel + maxContactRequests) | scaffold ser billetten (issuer, audienceToken, expiresAt); ikke `privateNotes` | `CellScaffold/…/VaporInviteLanding.swift:74` |
| 3 | Vegar → scaffold | `GET /invite/:token` | — | Vegar ser hilsen, `basis`-felter (**ny**, WP4), utløp, hjelp (**ny**, WP9). Scaffold setter `opened`; **vises ikke for K** (WP5) | `:230` |
| 4 | Vegar → scaffold | `POST /invite/:token/reply` | `HavenInviteContactRequest` (ja) · `decision: notNow` · `HavenInviteTombstone` (**ny**, WP5) · krav om retting/sletting (**ny**, WP3) | scaffold lagrer svaret; K ser bare `answered` for begge nei | `:334`, `:362` |
| 5 | scaffold → InvitationCell | `POST /api/invite/status`, `/requests` | `HavenInviteStatusReport`, kontaktforespørsler | K | `:172`, `:197` |
| 6 | InvitationCell (K) | `invite.acceptContactRequest` | relasjonspost K↔V | K | `InvitationCell.swift:995` |
| 7a/7b | → EntityAnchor(K), EntityAnchor(V) | `entity.batchPersist` | én konvolutt per entitet: relasjon, signert avtale, chronicle | hver sin; ingen skriving uten eierbevis | kap. 18 fase 4; `EntityBatchPersistEnvelope` |
| 8 | K → V | `ChatInvitationArtifact` | signert av K, adressert V sin identitet (domenets, WP1) | V | `ChatInvitationProofUtility.swift:211` |
| 9 | V → ChatCell(K) | `ChatInvitationAcceptance` | signert av V | K; ChatCell markerer V akseptert i `invitedIdentities` | `:306`, `ChatCellTests` |
| 10 | ChatCell ↔ begge | meldinger | konvolutt per mottaker, rekey ved medlemsendring | bare K og V | `ChatCell.swift` |
| 11 | EntityAnchor(V') → EntityAnchor(V) | `entity.moveHome` (**ny**, WP12) | eksport signert av V, import i app, peker igjen | V; K ser at samtalen fortsetter, ikke hvor den bor | — |

## Det som aldri går over noen kant

- `privateNotes` (formål R): kant 1 leser den ikke, kant 2 bærer den ikke, kant 3 viser den ikke.
- `opened` mot K (formål E/F, §6.5): kant 5 rapporterer `published | answered | expired | revoked`.
- Medlemskapsspørsmål (formål A1): ingen kant svarer «finnes dette endepunktet i HAVEN».
