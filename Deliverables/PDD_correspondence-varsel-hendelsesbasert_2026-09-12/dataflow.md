# Dataflyt — ny post → varsel (HD-0069, vei A)

Last verified against code: 2026-09-12 (kilder i FORMAALSSPEC.md §0 og VALIDERING.md). Kanter merket *ny* bygges i denne leveransen.

```mermaid
flowchart LR
  P[Motpart: vegar-local-agent / victoria-lille-robot] -- "HTTP message.send (eksisterende)" --> S[AssistantCorrespondenceCell på staging]
  S -- "FlowElement haven.assistant.correspondence.message.send / .ack, uten content, filtrert på recipientID (ny: WP-S1)" --> A[haven-agentd: CorrespondenceFlowSubscriber (ny: WP-A2)]
  A -- "AgentChallenge correspondence:<messageID> (ny: WP-A1)" --> C[Celle agent/challenges (ny: WP-A3)]
  C -- "FlowElement haven.agent.challenge.created|updated|resolved (ny)" --> M[HAVEN Agent.app: bro-klient (ny: WP-M1)]
  M -- "UNUserNotificationCenter (eksisterende ChallengeNotifier)" --> N[macOS varslingssenter]
  M -- "get / set over broen (ny)" --> C
  W[AdminWindow] -- "get / set over samme bro (ny: WP-M2)" --> C
  C -- "projeksjon (eksisterende rute)" --> J[GET /challenges JSON]
  L[Losen] -- "message.ack (eksisterende MCP, HTTP)" --> S
```

| # | Kant | Fra → til | Hendelse / endepunkt | Kontrakt / kilde | Status |
|---|---|---|---|---|---|
| 1 | Motpart sender | motpart → `AssistantCorrespondenceCell` | `message.send` (HTTP, scaffold-identitet som requester) | `CellScaffold::…/AssistantCorrespondenceContracts.swift`; `VaporAssistantCorrespondence.swift` l. 110–155 | finnes |
| 2 | Server sier fra | `AssistantCorrespondenceCell` → abonnent (daemon) | FlowElement `haven.assistant.correspondence.message.send` / `.message.ack`, topic `haven.assistant.correspondence`, uten `content`, filtrert på `recipientID` | WP-S1 (HD-0072); presedens `AgentConversationInboxCell`, `ChatCell.flow` | **ny** |
| 3 | WS-vei | daemon → staging | Sprout `native-porthole/:pubId/:bridgeId` med utgiver-allowlist, eller gjenopprettet bridgehead | WP-D1b (HD-0073); `VaporSproutResolver.swift` l. 60–79 | **driftsendring** |
| 4 | Abonnement | `CorrespondenceFlowSubscriber` → `BridgeBase.flow(requester:)` | én sesjon per principal; reconnect m/ backoff; catch-up `inbox.list(afterSequence)` én gang | WP-A2; `AgentConversationFlowSubscriber.swift` l. 118–196 | **ny** |
| 5 | Hendelse → sak | subscriber → `ChallengeInboxService` | `AgentChallenge` id `correspondence:<messageID>`, kind `agent-attention`, svar `open` / `dismiss-today`, `handleAt: assistant` | WP-A1; `Contracts/agent-challenge-v1.schema.json` (+ kilde `correspondence` fra grenen 11.9) | **ny** |
| 6 | Kvittering løser | `message.ack`-hendelse → sak `resolved` | samme abonnement som 4 | WP-A1 | **ny** |
| 7 | Innboksen som celle | providers → celle `agent/challenges` | `get` (innboks), `set` (respond, dismiss-today), FlowElement per endring | WP-A3; `contract/agent_challenges_cell_contract_v0.json` | **ny** |
| 8 | Bro app ↔ agent | HAVEN Agent.app → `bridgehead/agent-challenges/<bridgeId>` | WS-oppgradering med kontrollbro-token; `BridgeBase` + `LightweightBridgeTransport`; identitet fra WP-M0 | WP-M0/M1; `AgentControlBridgeServer.swift` l. 149–192; `AgentConfig.swift` l. 153–209 | **ny** (bridgehead finnes) |
| 9 | Varsel | app → macOS | `UNUserNotificationCenter`, kategori fra sakens svaralternativer, hemmelighetsfilter | eksisterende `ChallengeNotifier`, `ChallengeNotifierCategory` | finnes |
| 10 | Adminflate | `AdminWindow` → celle | `get`/`set` over samme bro | WP-M2 | **ny** |
| 11 | Projeksjon | celle → `GET /challenges` | samme provider, ingen egen bygging | `AgentControlBridgeServer.swift` l. 79–94 | finnes (blir projeksjon) |
| 12 | Kvittering | Losen (MCP) → server | `message.ack` over HTTP | `HavenAgentD::Sources/HavenCorrespondenceMCP/CorrespondenceClient.swift` (origin/main) | finnes |

Unntak som må stå åpent: kildene `scaffold-queue` og `agent-health` har ikke noe endringssignal i dag; WP-A3 dokumenterer hvordan cellen får endring fra dem uten skjult timer, eller merker dem som «lest på forespørsel» i kildestatus.
